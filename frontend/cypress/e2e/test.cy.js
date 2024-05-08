describe('Add a new task', () => {

    let uid // user id
    let name // name of the user (firstName + ' ' + lastName)
    let email // email of the user

    before(function () {        
        // create a fabricated user from a fixture
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

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/tasks/create',
                    form: true,
                    body: {
                        title: "Rick Astley - Never Gonna Give You Up",
                        description: "Popular 80's Song",
                        url: "dQw4w9WgXcQ",
                        userid: uid,
                        todos: "Watch video"
                    }
                })
            })
        })
    })

    beforeEach(function () {
        // Set the viewport to 1000px by 1000px
        cy.viewport(1000, 1000);
        // enter the main main page
        cy.visit('http://localhost:3000')
        // Login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()
        // Should now be successfully logged in
        
        //Click on Task
        cy.get('.title-overlay').last().click()
    })

    /* Use Case ID R8UC1 */

    it('1.1: Confirm "Add a new todo" item is empty', () => {
        cy.get('input[type=text]')
            .should('be.empty')
    })

    it('2.1: Confirm "Add" button is disabled', () => {
        cy.get('input[type=submit]')
            .should('be.disabled')
    })

    
    it('2.2: Confirm "Add" button is enabled when "Add a new todo" item is not empty', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('input[type=submit]')
            .should('be.enabled')
    })

    it('2.3: Confirm new (active) to-do item with the given description is appended to the bottom of the list of existing to-do items', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('.inline-form input[type=submit]')
            .click()
        cy.get('li.todo-item .editable')
            .last()
            .contains('Watch this video later')
            .should('be.visible')
    })

    /* Use Case ID R8UC2 */

    after(function () {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})
