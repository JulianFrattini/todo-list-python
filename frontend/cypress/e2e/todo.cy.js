describe('user can add, change state and delete todo items', () => {
    let uid
    let name
    let taskTitle
    let todoTitle

    before(() => {
        cy.fixture('user.json')
            .then((user) => {
                cy.request({
                    method: 'POST',
                    url: 'http://localhost:5000/users/create',
                    form: true,
                    body: user
                }).then((response) => {
                    uid = response.body._id.$oid
                    name = `${user.firstName} ${user.lastName}`

                    cy.visit('http://localhost:3000')
                    cy.contains('div', 'Email Address')
                        .find('input[type=text]')
                        .type(user.email)
                    cy.get('form')
                        .submit()

                    taskTitle = 'A fine testing item.'
                    cy.contains('div', 'Title')
                        .find('input[type=text]')
                        .type(`${taskTitle}`)
                    cy.get('form')
                        .submit()
                })
            })
    })

    after(() => {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    })

    beforeEach(() => {
        cy.fixture('user.json')
            .then((user) => {
                cy.visit('http://localhost:3000')
                cy.contains('div', 'Email Address')
                    .find('input[type=text]')
                    .type(user.email)
                cy.get('form')
                    .submit()

                cy.contains('div', taskTitle)
                    .click()
            })
    })

    it('adds todo when title is not empty', () => {
        todoTitle = 'non-empty title'
        cy.get('input[placeholder*="Add a new todo item"]')
            .type(todoTitle)
        cy.contains('Add')
            .click()
        cy.get('.todo-item')
            .eq(-1)
            .should('contain', todoTitle);
    })

    it('add button is disabled when title is empty', () => {
        cy.get('input[placeholder*="Add a new todo item"]')
            .should('have.value', '')
        cy.contains('Add').should('be.disabled')
    })

    it('sets item to done and strikes through the item title when user clicks icon in front of the title',
        () => {
        cy.contains(todoTitle).prev()
            .should('have.class', 'unchecked')
            .trigger('click')
        cy.contains(todoTitle).prev()
            .should('have.class', 'checked')
        cy.contains(todoTitle)
            .should('have.css', 'text-decoration')
            .and('include', 'line-through')
    })

    it('sets item to active and removes strikethrough from the item title when user clicks icon ' +
        'in front of the title when item is marked as done', () => {
        cy.contains(todoTitle).prev()
            .should('have.class', 'checked')
            .trigger('click')
        cy.contains(todoTitle).prev()
            .should('have.class', 'unchecked')
        cy.contains(todoTitle)
            .invoke('css', 'text-decoration')
            .should('not.include', 'line-through')
    })

    it('removes item from todo list when user clicks x "behind" the description', () => {
        cy.contains(todoTitle).next()
            .should('contain', '✖')
            .trigger('click')
        cy.get(todoTitle)
            .should('not.exist')
    })
})
