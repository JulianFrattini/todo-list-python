const backend_url = Cypress.env('BACKEND_URL')



describe('Create new todo', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let email // email of the user


  before(function () {
    // create a fabricated user from a fixture
    cy.fixture('user.json')
    .then((user) => {
        cy.request({
          method: 'POST',
          url: `${backend_url}/users/create`,
          form: true,
          body: user
        })
        .then((response) => {
          uid = response.body._id.$oid
          email = user.email

          cy.request({
            method: 'POST',
            url: `${backend_url}/tasks/create`,
            form: true,
            body: {
              'title': "My first task",
              'description': "Test description",
              'userid': uid,
              'url': 'testurl',
              'todos': "Watch test video" // inte helt säker på varför det måste vara string här, men det verkar funka (kollat mot databas) och array funkar inte
            }
          })
          .then((response)=> {
            cy.request({
              method: 'GET',
              url: `${backend_url}/users/bymail/${email}`,
            }).then((response) => {
                cy.log(response.body) 
            });
          })
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('/')
    cy.contains('div', 'Email Address')
          .find('input[type=text]')
          .type(email)
          cy.get('form')
          .submit()
    cy.get('.container')
      .contains('.title-overlay', 'My first task')
      .parents('a')
      .click()
  })

  it('check that todolist is loaded', () => {
    cy.get('.todo-list')
    .find('.todo-item').last()
    .find('.editable')
    .should('have.text', 'Watch test video')
  })

  after(function () {
    // clean up by deleting the user 
    // and associated tasks and todosfrom the database
    cy.request({
      method: 'DELETE',
      url: `${backend_url}/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})