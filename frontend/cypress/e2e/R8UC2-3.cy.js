describe('Logging into the system', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user
  let todoid
  
  beforeEach(function () {
      // create a fabricated user from a fixture
      cy.viewport(1480, 1000);
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
          cy.wait(3000)
          cy.request({
            method: 'GET',
            url: `http://localhost:5000/tasks/ofuser/${uid}`
          }).then((response) => {
            cy.log(response)
            todoid = response.body[0].todos[0]._id.$oid
          })
          //cy.wait(3000)
  
        })
      })
    })

    it('main success scenario is to set an active icon to inactive. should get line through, and toggle checked', () => {
      // Click on the second .checker element in the list
      cy.get('.todo-list > :nth-child(2) .checker').click()
      .should('have.class', 'checked')
      cy.get('.todo-list > :nth-child(2) .editable')
      .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)')
    })

    it('main success scenario is to set an inactive icon to active.should get off the line through, and toggle unchecked',() =>{
      console.log(todoid)
      cy.fixture("todo.json").then((todo) => {
          cy.request({
              method: 'PUT',
              url: `http://localhost:5000/todos/byid/${todoid}`,
              form: true,
              body: todo
            }).then((response) => {
              cy.log(response)
            })
        })
        cy.get('.todo-list > :nth-child(1) .checker').click()
        //cy.wait(2000)
        cy.get('.todo-list > :nth-child(1) .editable')
        .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)')
        cy.get('.todo-list > :nth-child(1) .checker')
        .should('have.class', 'checked')
        .click()
        .should('not.have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)')
    })

    
    it('mains success scenario to click on x icon of a todo item to remove the item(R8UC3)', ()=>{
      cy.get('ul.todo-list')
      .should('contain.text', 'myFirstTodoDescription')
      cy.get(':nth-child(2) > .remover').click()
      cy.get('ul.todo-list')
      .should('not.contain.text', 'myFirstTodoDescription')
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

