describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  

  beforeEach(function () {
    // create a fabricated user from a fixture
    cy.viewport(1000, 1600);
    cy.fixture('user.json').then((user) => {
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid
        name = user.firstName + ' ' + user.lastName
        email = user.email

        // enter the main main page
        cy.visit('http://localhost:3000')

        // make sure the landing page contains a header with "login"
        cy.get('h1')
          .should('contain.text', 'Login')

        // detect a div which contains "Email Address", find the input and type (in a declarative way)
        cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)

        // submit the form on this page
        cy.get('form')
          .submit()

        cy.contains('div', 'title')
        .find('input[type=text]')
        cy.get('#title')
        .type('myFirstTask')
        cy.get('[type="submit"]').click()

        // make sure conatiner have tha added task
        cy.get('.main > :nth-child(1)')
          .should('contain.text', 'myFirstTask')

        // show detail view mode
        cy.get(':nth-child(1) > a > img').trigger('click')

        // show detail view mode
      cy.get('.popup-inner').should('be.visible');
      // make sure the task page contains a header with "myFirstTask"
      cy.get('h1 > .editable').should('contain.text', 'myFirstTask')   
      })
    })
  })


  it('add button should be enabled when description is filled', () => {
    // click on the todo description
    cy.get('.inline-form > [type="text"]').click()
    // clear the todo description
    cy.get('.inline-form > [type="text"]').clear()
    // type the new todo description
    cy.get('.inline-form > [type="text"]').type('myFirstTodoDescription')

    // add button should be enabled
    cy.get('.inline-form > [type="submit"]').should('be.enabled')
  })
  
  it('main succs scenario add button should be disabled when description is empty', () => {
    // click on the todo description
    cy.get('.inline-form > [type="text"]').click()
    // clear the todo description
    cy.get('.inline-form > [type="text"]').clear()
    
    // add button should be disabled
    cy.get('.inline-form > [type="submit"]').should('be.disabled')
  })

  

  it('main success scenario add subtask to the bottom when description is filled and add button is enabled', () => {
    // click on the todo description
    cy.get('.inline-form > [type="text"]').click()
    // clear the todo description
    cy.get('.inline-form > [type="text"]').clear()

    // type the new todo description
    cy.get('.inline-form > [type="text"]').type('myFirstTodoDescription')
    // add button should be enabled
    cy.get('.inline-form > [type="submit"]').should('be.enabled')
    // click on the add button
    cy.get('.inline-form > [type="submit"]').click()

    // type the new todo description
    cy.get('.inline-form > [type="text"]').type('mySecondTodoDescription')
    // add button should be enabled
    cy.get('.inline-form > [type="submit"]').should('be.enabled')
    // click on the add button
    cy.get('.inline-form > [type="submit"]').click()
    
    // check that the subtask is added
    cy.get('.todo-list > :nth-child(3)').should('contain.text', 'mySecondTodoDescription')
    cy.get('.todo-list > :nth-child(3)').should('contain.text', 'mySecondTodoDescription')
    
  })
  
  it('main succs scenario add button should be disabled when description is empty', () => {
    // click on the todo description
    cy.get('.inline-form > [type="text"]').click()
    // clear the todo description
    cy.get('.inline-form > [type="text"]').clear()
    
    // add button should be disabled
    cy.get('.inline-form > [type="submit"]').should('be.disabled')
  })

  
  afterEach(function () {
    // clean up by deleting the user from the database 

    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })  
  })
})
