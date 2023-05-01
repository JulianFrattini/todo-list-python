describe('Logging into the system', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let taskTitle = 'Task#1'
    let todo1 = 'todo1'
    let todo2 = 'todo2'

    before(function () {
      // create a fabricated user from a fixture
      cy.fixture('user.json')
        .then((user) => {
          cy.request({
            method: 'POST',
            url: 'http://localhost:5000/users/create',
            // url: 'http://localhost:27017/users/create',
            form: true,
            body: user
          }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
          })
        })
    })

    beforeEach(function () {
      // enter the main main page
      cy.visit('http://localhost:3000')
    })

    it('starting out on the landing screen', () => {
      // make sure the landing page contains a header with "login"
      cy.get('h1')
        .should('contain.text', 'Login')
    })

    it('login to the system with an existing account', () => {
      // detect a div which contains "Email Address", find the input and type (in a declarative way)
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com')
      // alternative, imperative way of detecting that input field
      //cy.get('.inputwrapper #email')
      //    .type('mon.doe@gmail.com')

      // submit the form on this page
      cy.get('form')
        .submit()

      // assert that the user is now logged in
      cy.get('h1')
        .should('contain.text', 'Your tasks, ' + name)

      // If you do not want status codes to cause failures pass the option: failOnStatusCode: false

      //  ******************** R8UC1 *************************

      cy.get('.inputwrapper #title')
        .type(taskTitle)

      cy.get('form')
        .submit()

      cy.contains('div', taskTitle)
        .should('contain.text', taskTitle)
        .click()

      // Add button should be disabled
      cy.get('.popup-inner')
        .find('input[value="Add"]')
        .should('be.disabled')

      cy.get('.popup-inner')
        .find('input[type="text"]')
        .type(todo1)
        .should('be.visible')

      cy.get('.popup-inner')
        .find('input[value="Add"]')
        .should('be.enabled')

      cy.get('input[value="Add"]').click()
      cy.get('.todo-list').children('.todo-item').should('have.length',2)
      cy.get('.todo-list').children('.todo-item').should('contain.text',todo1)
    })

    //  ******************** R8UC2 *************************
    it('edit todo-item from an existing account', () => {
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com{enter}')

      cy.get('.container-element')
        .find('a')
        .first().click()

      cy.get('ul')
        .should('have.class', 'todo-list')

      cy.get('.todo-list > li').should(($lis) => {
        expect($lis).to.have.length(3)
        expect($lis.eq(0)).to.contain('Watch video')
        expect($lis.eq(1)).to.contain(todo1)
      })
      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('span').first().should('have.class', 'checker unchecked')


      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('span').first().click()

        // get AssertionError
      // cy.get('.todo-list > .todo-item').first()
      //   .find('.checker').should('have.class', 'checker checked')

    })

    it('todo-item class=checker tobe checked', () =>{
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com{enter}')

      cy.get('.container-element')
        .find('a')
        .first().click()

      cy.get('ul')
        .should('have.class', 'todo-list')

      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('.checker').first().should('have.class', 'checker checked')
    })
    //  ******************** R8UC3 *************************
    it('the user clicks X to delete a todo item', () => {
      // detect a div which contains "Email Address", find the input and type (in a declarative way)
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com{enter}')

      cy.get('.container-element')
        .find('a')
        .first().click()

      cy.get('ul')
        .should('have.class', 'todo-list')

      cy.get('.todo-list > li').should(($lis) => {
        expect($lis.eq(0)).to.contain('Watch video')
        expect($lis.eq(1)).to.contain(todo1)
      })
      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('.remover').click()

      cy.get('.todo-list > li').should(($lis) => {
        expect($lis).not.to.contain('Watch video')
      })
    })

    after(function () {
      // clean up by deleting the user from the databaseg
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
        // url: `http://localhost:27017/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  })
