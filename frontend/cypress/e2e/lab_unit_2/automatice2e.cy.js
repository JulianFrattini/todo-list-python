describe('Todo List Manipulation with Task Creation', () => {
  let uid;
  let name = 'James Doe';
  let email = 'james.doe@gmail.com';
  let taskTitle = 'New Task Test';
  let newItem = 'Cypress Test';

  before(function () {
    // Skapar användare från en fixtur
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid;
        name = `${user.firstName} ${user.lastName}`;
        email = user.email;
      });
    });
  });

  beforeEach(function () {
    // Loggar in användaren
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('h1').should('contain.text', `Your tasks, ${name}`);
  });

  it('creates a new task', () => {
    cy.contains('div', 'Title').find('input[type=text]').type(taskTitle, {force: true});
    cy.get('input[type=submit]').click({force: true});
  });

  it('check if add-button is disabled', () => {
    cy.contains('div.title-overlay', taskTitle).click({force: true});
    cy.get('form.inline-form').find('input[type=submit]').should('be.disabled');
  });

  it('accesses a task, check add-button and add a todo item', () => {
    cy.contains('div.title-overlay', taskTitle).click({force: true});
    cy.get('form.inline-form').find('input[type=text]').type(newItem, {force: true});
    cy.get('form.inline-form').find('input[type=submit]').should('be.enabled');
    cy.get('form.inline-form').find('input[type=submit]').click({force: true});
  });

  it('check if item exists', () => {
    cy.contains('div.title-overlay', taskTitle).click({force: true});
    cy.get('li.todo-item').should('contain.text', newItem);
  });

  // it('check if add-button is enabled', () => {
  //   cy.contains('div.title-overlay', taskTitle).click({force: true});
  //   cy.get('form.inline-form').find('input[type=submit]').should('be.enabled');
  // });

  it('check if toggle is unchecked', () => {
    cy.contains('div.title-overlay', taskTitle).click();
    cy.contains('li.todo-item', 'Cypress Test').find('span.checker').should('have.class', 'unchecked');
  });

  it('toggle a todo item', () => {
    cy.contains('div.title-overlay', taskTitle).click();
    cy.contains('li.todo-item', 'Cypress Test').find('span.checker').first().click({force: true});
  });

  it('check if toggle is checked', () => {
    cy.contains('div.title-overlay', taskTitle).click();
    cy.contains('li.todo-item', 'Cypress Test').find('span.checker').should('have.class', 'checked');
  });

  it('delete a todo item', () => {
    cy.contains('div.title-overlay', taskTitle).click();
    cy.contains('li.todo-item', 'Cypress Test').find('span.remover').first().click({force: true});
    cy.get('li.todo-item').should('not.contain.text', newItem);
  });

  it('check if todo item is deleted', () => {
    cy.contains('div.title-overlay', taskTitle).click();
    cy.get('li.todo-item').should('not.contain.text', newItem);
  });

  after(function () {
    // Radera användare
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    });
  });
});
