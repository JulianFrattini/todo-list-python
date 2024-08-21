describe('Logging into the system', () => {

    let uid
    let name
    let email

    before(function () {
        // Create a user
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

    beforeEach(function () {
        // Login to the system
        cy.visit('http://localhost:3000')

        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)
        cy.get('form')
            .submit()

        // Using POST to create a task
        cy.request({
            method: 'POST',
            url: 'http://localhost:5000/tasks/create',
            form: true,
            body: {
            'title': "new task",
            'description': "description",
            'userid': uid,
            'url': "http://example.com",
            'todos': ""
            }
        })
        .then((response) => {
            cy.log('Task created', response.body)
        })
    })

    it('R8UC1: Add button disabled when description empty', () => {

        cy.get('.container')
            .contains('.title-overlay', 'new task')
            .parents('a')
            .click()

        cy.get('.todo-list')
            .find('.inline-form')
            .find('input[type=text]')
            .get('.inline-form input[value="Add"]')
            .should('be.disabled')
        //Assertion error: expected Add button to be disabled, which is correct..?
    })

    it('R8UC1: Adding a todo to a task', () => {

        cy.get('.container')
            .contains('.title-overlay', 'new task')
            .parents('a')
            .click()

        cy.get('.todo-list')
            .find('.inline-form')
            .find('input[type=text]')
            .type('new todo')
            .get('.inline-form input[value="Add"]')
            .click()
            .get('.todo-list')
            .find('.todo-item').last()
            .find('.editable')
            .should('have.text', 'new todo')
    })

    it('R8UC2: Setting a todo item to done', () => {

        cy.get('.container')
            .contains('.title-overlay', 'new task')
            .parents('a')
            .click()
            
        cy.get('.todo-list .todo-item')
            .contains('.editable', 'new todo')
            .parent()
            .find('.checker.unchecked')
            .click()

        cy.get('.todo-item')
            .contains('.editable', 'new todo')
            .should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)')
    })

    it('R8UC2: Setting a todo item back to active', () => {

        cy.get('.container')
            .contains('.title-overlay', 'new task')
            .parents('a')
            .click()
        
        cy.get('.todo-list .todo-item')
            .contains('.editable', 'new todo')
            .parent()
            .as('todoItem')
    
        cy.get('@todoItem')
            .find('.checker.checked')
            .click()
    
        cy.get('@todoItem')
            .find('.editable')
            .should('not.have.css', 'text-decoration', 'line-through')
    })

    it('R8UC3: Deleting a todo item from task', () => {
            
        cy.get('.container')
            .contains('.title-overlay', 'new task')
            .parents('a')
            .click()

        cy.get('.todo-list .todo-item')
            .contains('.editable', 'new todo')
            .parent()
            .find('.remover')
            .click()

        cy.get('.todo-list')
            .should('not.contain', 'new todo')
    })

    after(function () {
        // Using DELETE to delete the user
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`,
        }).then((response) => {
            // Make sure that user is deleted after
            cy.log('User deleted', response.status);
        })
    })
})