describe('Deleting a todo of a task', () => {
  // define variables that we need on multiple occasions
  let uid // user id
  let name // name of the user (firstName + ' ' + lastName)
  let email // email of the user

  let oldTestUserID
  let taskID // id of the task

  before(function () {
    // find potential old test user
    cy.request({
      method: 'GET',
      url: 'http://localhost:5000/users/all'
    }).then((response) => {
      cy.log('body length:', response.body.length)
      if (response.body.length > 0) {
        const oldTestUserEmail = 'mon.doe@gmail.com'
        const oldTestUser = response.body.find(user => user.email === oldTestUserEmail)
        cy.log(oldTestUserEmail)

        if (oldTestUser) {
          oldTestUserID = oldTestUser._id.$oid

          cy.log('old id', oldTestUserID)

          // clean up state by deleting the user from the database
          cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${oldTestUserID}`
          }).then((response) => {
            cy.log(response.body)
          })
        }
      }
    })

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

    // create a task from a fixture
    cy.fixture('task.json')
      .then((task) => {
        let data = {
          ...task,
          userid: uid
        }
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/tasks/create',
          form: true,
          body: data
        }).then((response) => {
          taskID = response.body
          console.log(taskID)
        })
      })
  })

  beforeEach(function () {
    // enter the main main page
    cy.visit('http://localhost:3000')

    // enter email into field
    cy.contains('div', 'Email Address')
      .find('input[type=text]')
      .type(email)

    // submit the form on this page
    cy.get('form')
      .submit()

    // find the todo and click it
    cy.get('div.container-element')
      .find('a')
      .click()
  })

  it('prepare for 1.1 by clicking X', () => {
    // Find the todo item
    cy.contains('.todo-item', 'Watch video')
      // Find the X button and click on it
      .find('.remover')
      .click();
  })

  it('1.1: the todo is removed by clicking X', () => {
    // After clicking X, assert that the todo is removed
    cy.contains('.todo-item', 'Watch video')
      .should('not.exist')
  })
})
