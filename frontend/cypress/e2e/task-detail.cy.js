describe('Adding and editing todo items', () => {
    // define variables that we need on multiple occasions
    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user

    let taskTitle // title of task from file

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

                taskTitle = task.title
            })

        cy.viewport(1024, 768)
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
        cy.contains('div', taskTitle)
            .click()
    })

    /**
 * test cases
 * 
 */

    it('assert Add button is disabled (input field empty)', () => {
        // Check state of Add button
        cy.get('input[type=submit][value=Add]')
            .should('be.disabled')
        // .should('be.enabled')
    })

    it('assert Add button is enabled (input field populated)', () => {
        // Populate input field
        cy.get('ul.todo-list')
            .find('input[type=text]')
            .type('test 1')

        cy.get('input[type=submit][value=Add]')
            .should('be.enabled')
    })

    it('assert new todo item is cretad when discrpition is filled and "Add" is pressed', () => {
        // Populate input field
        cy.get('ul.todo-list')
            .find('input[type=text]')
            .type('test 1')

        // Click Add button
        cy.get('input[type=submit][value=Add]')
            .click()

        // Assert todo list contains text of newly added item
        cy.get('ul.todo-list').should('contain.text', 'test 1')
    })

    it('assert done todo item set to active when clicked', () => {
        //check that the chosen item is unchecked
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.unchecked')

        // Click checker span of newly created item
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.checker')
            .click()

        // Check that description span has line-through css property
        cy.get('li.todo-item').contains('test 1')
            .invoke('css', 'text-decoration')
            .should('contain', 'line-through')
    })

    it('assert active todo item set to done when clicked', () => {
        //check that the chosen item is checked
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.checked')

        // Click checker span of newly created item
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.checker')
            .click()

        //check that the chosen item is unchecked
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.unchecked')
    })

    it('use x button to remove task', () => {
        //check that there are the right amount of todo items
        cy.get('li.todo-item')
            .should('have.length', 2)

        // Click remover span of test 1 to remove it
        cy.get('li.todo-item')
            .contains('test 1')
            .parent('li')
            .find('span.remover')
            .click()

        //one item should remain
        cy.get('li.todo-item')
            .should('have.length', 1)
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