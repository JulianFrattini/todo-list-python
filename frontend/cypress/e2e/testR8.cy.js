describe('GUI Testing by manipulating a todo item', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let taskTitle = 'GUI Test'
    let todo1 = 'gui-todo1'

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
          })
        })
    })

    beforeEach(function () {
      // enter the main main page
      cy.visit('http://localhost:3000')
    })

    it('starting out on the landing screen', () => {
      cy.get('h1')
        .should('contain.text', 'Login')
    })

    it('login to the system with an existing account', () => {
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com')

      // submit the form on this page
      cy.get('form')
        .submit()

      // assert that the user is now logged in
      cy.get('h1')
        .should('contain.text', 'Your tasks, ' + name)


      //  ******************** R8UC1 *************************

      cy.get('.inputwrapper #title')
        .type(taskTitle)

      cy.get('form')
        .submit()

      cy.contains('div', taskTitle)
        .should('contain.text', taskTitle)
        .click()

      // ***** UC1 *****
      // ***** Scenario 1: TC1 *****
      cy.get('.popup-inner').find('form', '.inline-form')
      .should('have.class', 'inline-form')
      .then($form => {
        if ($form.find('input').length > 0) {
          return true;
        } else {
          // input field is not present
          return false;
        }
      })

      // ***** Scenario 1: TC2 *****
      cy.get('.inline-form')
      .find('input[type="text"]').as('todoInput')
      .should('exist')

      // ***** Scenario 2: TC1 *****

      // check if description field is Empty or not empty.
      cy.get('@todoInput')
      .should('have.value', '')

      cy.get('.popup-inner').find('.todo-list')
      .find('input[value="Add"]').as('add')
      .should('be.disabled')

      cy.get('@todoInput')
        .type(todo1, {force: true})
        .should('not.have.value', '')

      cy.get('@add').should('be.enabled')

      // ****** Scenario2 ***** //

      // Action 'Click' on 'Add'
      cy.get('@add').click()

      // Check expected outcome: check if new-todo item exist at the bottom of the list.
      cy.get('.todo-list').children('.todo-item').last()
        .should('contain.text',todo1)
    })

    //  ******************** R8UC2 *************************
    it('UC2: click on icon in front of a todo-item', () => {
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com{enter}')

      cy.get('.container-element')
        .find('a')
        .first().click()

      //tocheck the toggle if struck through or not!
      cy.get('.todo-list').first()
        .find('.todo-item').first().as('todoItem')
        .find('span.editable').as('todoName')
        .should('not.have.css', 'text-decoration', 'line-through');

    //   cy.pause() // this will activate the line-through

      cy.get('@todoItem')
        .find('span.checker').click()

      cy.get('@todoName')
      .should('be.visible')
      .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)');

    })

    //  ******************** R8UC3 *************************
    it('UC3: the user clicks X to delete a todo item', () => {
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
  // check if the X is visible, enabled and clickable
      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('.remover')
        .should('contain.text', '✖').as('delete');

      cy.get('@delete').click()

      cy.get('.todo-list > li').should(($lis) => {
        expect($lis.eq(0)).not.to.contain('Watch video')
      })
    })

    after(function () {
      // clean up by deleting the user from the databaseg
      cy.request({
        method: 'DELETE',
        url: `http://localhost:5000/users/${uid}`
      }).then((response) => {
        cy.log(response.body)
      })
    })
  })
