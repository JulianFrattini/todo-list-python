describe('Adding a todo to an added task. .', () => {
    let uid
    let name
    let email // create a fabricated user from a fixture
    before(function() {

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

                    cy.visit('http://localhost:3000')


                    cy.contains('div', 'Email Address') // Log into the site
                        .find('input[type=text]')
                        .type(email)
                        // submit the form on this page
                    cy.get('form')
                        .submit()

                    cy.get('.inputwrapper #title') // Adding the task
                        .type("Test title")
                    cy.get('.inputwrapper #url')
                        .type("LB8KwiiUGy0")
                    cy.get('form')
                        .submit()
                })
            })

    })


    beforeEach(function() {
        // enter the main main page and log in
        cy.visit('http://localhost:3000')


        cy.contains('div', 'Email Address') // Log into the site
            .find('input[type=text]')
            .type(email)
            // submit the form on this page
        cy.get('form')
            .submit()



    })





    it('Adding a todo to an added task. .', () => {
        cy.contains('Test title')
            .click()
        cy.get('.inline-form')
            .find('input[type=text]')
            .type("Test todo item", { force: true })
        cy.get('.inline-form').submit()

        cy.get('.todo-list')
            .should('contain.text', 'Test todo item')

    })

    it('The todo is struck through when the icon for doing it is clicked, and the icon turns into a check mark.', () => {
        cy.contains('Test title')
            .click()
        cy.contains('Test todo item')
            .get('.checker')
            .click({ multiple: true })

        cy.contains("Test todo item")
            .should(($element) => {
                expect($element).to.have.css('text-decoration').match(/line-through/);
            })

        cy.get('.checker')
            .should('have.class', 'checked')



    })

    after(function() {
        // clean up by deleting the user from the database
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })


    })

})