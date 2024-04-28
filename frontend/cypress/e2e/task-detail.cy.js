describe('Adding and editing todo items', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user
  
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

        cy.fixture('task.json')
            // Create a fabricated task
            .then((task) => {
                task.userid = uid

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/tasks/create',
                    form: true,
                    body: task
                })
            })
    })
  
    beforeEach(function () {
        // Login and go to task overview
        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()

        // Click fabricated task to go into detail view
        cy.contains('div', 'Cypress testing')
            .click()
    })

    /*
    it('assert Add button is enabled (input field populated)', () => {
        // Populate input field
        cy.get('ul.todo-list')
            .find('input[type=text]')
            .type('test')

        // Check state of Add button
        cy.get('input[type=submit][value=Add]')
            .should('be.enabled')
    })

    it('assert new todo item not added when Add button clicked (input field empty)', () => {
        // Click Add button
        cy.get('input[type=submit][value=Add]')
            .click()

        // Assert length of todo list is not greater than default (2)
        cy.get('ul.todo-list')
            .find('li')
            .should('have.length', 2)
            // .should('have.length', 3)
    })
    */

    it('assert Add button is disabled (input field empty)', () => {
        // Check state of Add button
        cy.get('input[type=submit][value=Add]')
            .should('be.disabled')
            // .should('be.enabled')
    })

    it('assert new todo item added when Add button clicked (input field populated)', () => {
        // Populate input field
        cy.get('ul.todo-list')
            .find('input[type=text]')
            .type('test')

        // Click Add button
        cy.get('input[type=submit][value=Add]')
            .click()

        // Assert todo list contains text of newly added item
        cy.get('ul.todo-list').should('contain.text', 'test')
    })

    after(function () {
        // Delete user (automatically deletes user's tasks and todos?)
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
            }).then((response) => {
                cy.log(response.body)
        })
    })

})