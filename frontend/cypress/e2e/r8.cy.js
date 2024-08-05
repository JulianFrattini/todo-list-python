/**
 * As an authenticated user I want to manipulate the todolist associated to a task, i.e., add a new, toggle an existing, or delete an existing todo item.
**/

describe('R8UC1: Create a task', () => {
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  before(() => {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  after(() => {
    cy.deleteUser(uid);
  });

  beforeEach(() => {
    cy.login(email);
  });

  it('Should display task', () => {
    cy.get('h1').contains('Your tasks, ');
    // check if the task is displayed
    cy.get('.container-element').children('a').should('exist');
  });

  it('Should add a new todo item if input is not empty', () => {
    // Add a new todo item
    cy.get('input[name="title"]').type('New todo item');
    cy.get('input[type=submit]').contains('Create new Task').should('not.be.disabled').click();

    // Verify the new todo item is appended to the list
    cy.get('.container-element').children('a').last().should('contain', 'New todo item');
  });

  it('Should not add a new todo item if input is empty', () => {
    // Ensure the input field is empty
    cy.get('input[name="title"]').clear();

    // Verify the Add button is disabled
    cy.get('input[type=submit]').contains('Create new Task').should('be.disabled');
  });

});

describe('R8UC2: Toggle task todo', () => {
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  after(() => {
    cy.deleteUser(uid);
  });

  before(() => {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.login(email);
    cy.addTask({
      title: "Hello Task",
      description: "Task 1 description",
      userid: uid,
      url: "ahmad",
      todos: "watch video"
    });

    // click on the last item
    cy.get('h1').contains('Your tasks, ');
    cy.get('.container-element').children('a').last().click();
    // Check if the task is displayed
    cy.get('.popup-inner').contains('Hello Task');
  });

  it('Toggle from active to done', () => {
      cy.get('span.checker').should('have.class', 'unchecked').first().as('checkerElem');
      cy.get('span.editable').first().as('titleElem');
      cy.get('@checkerElem').click();
      cy.get('@checkerElem').should('have.class', 'checked');
      cy.get('@titleElem').should('have.css', 'text-decoration', 'line-through');
  });
  it('Toggle from active to done', () => {
      cy.get('span.checker').should('have.class', 'checked').first().as('checkerElem');
      cy.get('span.editable').first().as('titleElem');
      cy.get('@checkerElem').click();
      cy.get('@checkerElem').should('have.class', 'unchecked');
      cy.get('@titleElem').should('not.have.css', 'text-decoration', 'line-through');
  });

});

describe('R8UC2: Delete task todo', () => {
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  after(() => {
    cy.deleteUser(uid);
  });

  before(() => {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
          uid = response.body._id.$oid
          name = user.firstName + ' ' + user.lastName
          email = user.email
        })
      })
  })

  beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.login(email);
    cy.addTask({
      title: "Hello Task",
      description: "Task 1 description",
      userid: uid,
      url: "ahmad",
      todos: "watch video"
    });

    // click on the last item
    cy.get('h1').contains('Your tasks, ');
    cy.get('.container-element').children('a').last().click();
    // Check if the task is displayed
    cy.get('.popup-inner').contains('Hello Task');
  });

  it('Remove a todo item', () => {
    cy.get('li.todo-item').first().as('todoItem');

    cy.get('span.remover').first().as('removerElem');
    cy.get('@removerElem').click();
    cy.get('@todoItem').should('not.exist');
  });

});
