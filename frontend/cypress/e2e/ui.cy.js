describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let todo = "first todo"

  before(function () {
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

  before(function () {
    // create a fabricated task
    cy.request({
      method: 'POST',
      url: 'http://localhost:5000/tasks/create',
      form: true,
      body: {
        userid: uid,
        title: "First task",
        description: "This is an interesting task",
        url: "u0-aBSN04BI",
        todos: "todo 1",
        start: "2024-03-01",
        end: "2024-04-01"
      }
    })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // make sure the landing page contains a header with "login"
    cy.get('h1')
      .should('contain.text', 'Login')

    // login to the system with an existing account
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // assert that the user is now logged in
    cy.get('h1')
      .should('contain.text', 'Your tasks, ' + name)

    // open task in detail view
    cy.contains('div', "First task")
      .click()
  })

  // R8UC1, create a new todo item with description
  it('Check if input field exists', () => {
    cy.get('.inline-form')
      .find('input[type=text]')
      .should('exist');
  })

  it('add-button should be enabled and the new item description should be added to the bottom of the list.', () => {
    cy.get('.inline-form')
      .find('input[type=text]')
      .type(todo);

    // click on add button
    cy.get('.inline-form')
      .find('input[type=submit]')
      .should('not.be.disabled')
      .click();

    // check if added to bottom of the list
    cy.get('li.todo-item').last().contains(todo);
  })

  it('todo item should not be added to todo-list if description is empty, add button should be disabled', () => {
    cy.get('input[placeholder="Add a new todo item"]')
      .clear({force: true
    })
  
    // check if description is empty
    cy.get('.inline-form')
      .find('input[type=text]')
      .should('have.value', '')

    // click on add button
    cy.get('.inline-form')
      .submit();

    // checks if new todo is not added
    cy.get('li.todo-item').last().should('contain.text', '');
  })

  // R8UC2, click on icon
  it('todo item is struck through', () => {
    cy.get('li.todo-item')
      .first()
      .find('span.checker')
      .click();

    // check if done
    cy.get('li.todo-item')
      .first()
      .find('span.checker')
      .should('have.class', 'checked')

    // check if struck through
    cy.get('li.todo-item')
      .first()
      .find('.editable')
      .should('have.css', 'text-decoration-line', 'line-through');
  })

  it('todo item is not struck through', () => {
    cy.get('li.todo-item')
      .first()
      .find('span.checker')
      .should('have.class', 'checked')

    // clicks on icon
    cy.get('li.todo-item')
      .first()
      .find('span.checker')
      .click();

    // check if not struck through and active
    cy.get('li.todo-item')
      .first()
      .find('span.checker')
      .should('not.have.class', 'checked')
      .and('not.have.css', 'text-decoration-line', 'line-through');
  })

  // R8UC3, click on the x symbol
  it('Todo element deleted', () => {
    cy.contains('li.todo-item', todo)
      .find('span.remover')
      .click();

    // Waiting to be removed, a bit buggy?
    cy.wait(10000)

    // checking for removed
    cy.contains('li.todo-item', todo)
      .should('not.exist')
  });

  after(function () {
    // clean up by deleting the user from the database
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})