describe('Test: todo', () => {
    // Define variables that we need on multiple occasions
    let uid // user id
    let email // email of the user

    before(function () {
        // Create a fabricated user from a fixture
        cy.fixture('user.json').then((user) => {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5000/users/create',
                form: true,
                body: user
            }).then((response) => {
                uid = response.body._id.$oid
                email = user.email

                let data = {
                    title: "Test Title",
                    description: "Test Song",
                    url: "dQw4w9WgXcQ",
                    userid: uid,
                    todos: "watch video"
                };

                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/tasks/create',
                    form: true,
                    body: data
                })
            })
        })
    })

    beforeEach(function () {
        // Enter the main page
        cy.visit('http://localhost:3000')
        // Login
        cy.contains('div', 'Email Address')
            .find('input[type=text]')
            .type(email)

        cy.get('form')
            .submit()
        // Should now be successfully logged in
        
        // Click on Task
        cy.get('.title-overlay').click()
    })

    it('1.1: Confirm the "Description" input field is empty.', () => {
        cy.get('.popup input[type=text]')
            .should('be.empty')
    })

    it('2.1: Confirm "Add" button is disabled.', () => {
        cy.get('.popup input[type=submit]')
            .should('be.disabled')
    })

    it('2.2: Confirm "Add" button is enabled when "Add a new todo item" is not empty.', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('input[type=submit]')
            .should('be.enabled')
    })

    it('2.3: Confirm new (active) todo item with the given description is appended to the bottom of the list of existing todo items.', () => {
        cy.get('.inline-form input[type=text]')
            .type('Watch this video later')
        cy.get('.inline-form input[type=submit]')
            .click()
        cy.get('li.todo-item .editable')
            .last()
            .contains('Watch this video later')
            .should('be.visible')
            .should(($element) => {
                const textDecoration = $element.css('text-decoration')
                expect(textDecoration).to.include('none')
            })
    })

    it('3.1: Icon in front of (active) todo is clicked and is set to "done". Toggled item is struck through.', () => {
        cy.get('li.todo-item span.checker.unchecked')
            .first()
            .click()
        cy.get('li.todo-item span.checker.checked')
            .first()
            .should('exist');
        cy.get('li.todo-item span.editable')
            .first()
            .should(($element) => {
                const textDecoration = $element.css('text-decoration')
                expect(textDecoration).to.include('line-through')
            })
    })

    it('3.2: Icon in front of (done) todo is clicked and is set to "active". Toggled item is not struck through.', () => {
        cy.get('.checker.unchecked')
            .click()
        cy.get('.checker.checked')
            .click()
        cy.get('.checker.unchecked')
            .should('exist');

        cy.get('li.todo-item span.editable')
            .should(($element) => {
                const textDecoration = $element.css('text-decoration')
                expect(textDecoration).to.include('none')
            })
    })

    it('4.1: Confirm that todo item is removed when deleted.', () => {
        cy.get('.remover')
            .first()
            .click()
        cy.contains('div', 'watch video')
            .should('not.exist')
    })

    after(function () {
        // Clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })
})
