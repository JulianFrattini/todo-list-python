describe('Logging into the system', () => {
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

      // ***** UC1 *****
      // ***** Scenario 1: TC1 *****
      cy.get('.inline-form')
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
      .should('have.class', 'inline-form')
      .find('input')
      .should('exist')

      // ***** Scenario 2: TC1 *****

      // TODO..test check if description field is Empty or not empty.
      cy.get('.inline-form')
      .should('have.class', 'inline-form')
      .find('input')
      .should('have.value', '')

      // 'Add' button should be disabled
      cy.get('.popup-inner')
      .find('input[value="Add"]')
      .should('be.disabled')

      // Description field should contain the input-text
      cy.get('.popup-inner')
      .find('input[type="text"]')
      .type(todo1)
      .should('not.have.value', '')

      // 'Add' button should be enabled now.
      cy.get('.popup-inner')
      .find('input[value="Add"]')
      .should('be.enabled')

      // ****** Scenario2 ***** //

      // Action 'Click' on 'Add'
      cy.get('input[value="Add"]').click()

      // Check expected outcome: check if new-todo item exist at the bottom of the list.
      cy.get('.todo-list').children('.todo-item')
        .last()
        .should('contain.text',todo1)
    })

    //  ******************** R8UC2 *************************
    it('click the icon in front of a todo-item', () => {
      cy.contains('div', 'Email Address')
        .find('input[type=text]')
        .type('mon.doe@gmail.com{enter}')

      cy.get('.container-element')
        .find('a')
        .first().click()

      //tocheck the toggle if struck through or not!
      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('span.editable')
        // .should('have.class', 'checker unchecked')
        .should('not.have.css', 'text-decoration', 'line-through');

      cy.pause() // this will activate the line-through

      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('span.checker').click()

      cy.get('.todo-list').first()
        .find('.todo-item').first()
        .find('span.editable')
        .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)');
      })


    //   cy.get('ul')
    //     .should('have.class', 'todo-list')

    //   cy.get('.todo-list > li').should(($lis) => {
    //     expect($lis).to.have.length(3)
    //     expect($lis.eq(0)).to.contain('Watch video')
    //     expect($lis.eq(1)).to.contain(todo1)
    //   })

    //     // get AssertionError
    //   // cy.get('.todo-list > .todo-item').first()
    //   //   .find('.checker').should('have.class', 'checker checked')

    // })

    // it('todo-item class=checker tobe checked', () =>{
    //   cy.contains('div', 'Email Address')
    //     .find('input[type=text]')
    //     .type('mon.doe@gmail.com{enter}')

    //   cy.get('.container-element')
    //     .find('a')
    //     .first().click()

    //   cy.get('ul')
    //     .should('have.class', 'todo-list')

    //   cy.get('.todo-list').first()
    //     .find('.todo-item').first()
    //     .find('.checker').first().should('have.class', 'checker checked')
    // })
    // //  ******************** R8UC3 *************************
    // it('the user clicks X to delete a todo item', () => {
    //   // detect a div which contains "Email Address", find the input and type (in a declarative way)
    //   cy.contains('div', 'Email Address')
    //     .find('input[type=text]')
    //     .type('mon.doe@gmail.com{enter}')

    //   cy.get('.container-element')
    //     .find('a')
    //     .first().click()

    //   cy.get('ul')
    //     .should('have.class', 'todo-list')

    //   cy.get('.todo-list > li').should(($lis) => {
    //     expect($lis.eq(0)).to.contain('Watch video')
    //     expect($lis.eq(1)).to.contain(todo1)
    //   })

    //   // check if the X is visible, enabled and clickable
    //   // cy.get('.todo-list').first()
    //   //   .find('.todo-item').first()
    //   //   .find('span')
    //   //   .find('.remover').should('be.clickable');

    //   cy.get('.todo-list').first()
    //     .find('.todo-item').first()
    //     .find('.remover').click()

    //   cy.get('.todo-list > li').should(($lis) => {
    //     expect($lis).not.to.contain('Watch video')
    //   })
    // })

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
