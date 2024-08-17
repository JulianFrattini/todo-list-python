describe('Configure tasks', () => {
    let taskvideo = 'https://www.youtube.com/watch?v=u8vMu7viCm8'
    let tasktitle = 'Test 12'
    let todotask = 'Watch 5 minutes of the video'

    beforeEach(function () {
        cy.createUser()
        cy.get('@userEmail').then((email) => {
        cy.login(email) 
        })

        // Making a task that will be used for UC1 UC2 and UC3
        cy.get('input[name=title]').type(tasktitle)
        cy.get('input[name=url]').type(taskvideo)
        cy.get('form').submit()
        cy.get('.title-overlay').contains(tasktitle).click()
    })

    // UC1 - TASK DESCRIPTIONS

    it('Adding a description to a task', () => {
        cy.get('input[placeholder="Add a new todo item"]').type(todotask, { force: true })
        cy.get('input[type="submit"][value="Add"]').click({ force: true })
        cy.get('.todo-item').should('contain.text', todotask)
    })
    
    it('Add button is disabled when the description is empty', () => {
        cy.get('input[placeholder="Add a new todo item"]').should('be.empty')
        cy.get('input[type="submit"][value="Add"]').should('be.disabled')
    })
    
    // UC2 - EDIT TASKS
 
    it('Check the task', () => {
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').click()
        //cy.get('ul.todo-list li.todo-item').first().find('span.checker').click()
    
        cy.get('ul.todo-list li.todo-item').first().find('span.checker')
        .should('have.class', 'checked')
    })


    it('Uncheck the task', () => {
        cy.get('ul.todo-list li.todo-item').first().find('span.checker').click()
        //cy.get('ul.todo-list li.todo-item').first().find('span.checker').click()
        
        cy.get('ul.todo-list li.todo-item').first().find('span.checker')
        .should('have.class', 'unchecked')
    })

    
    // UC3 - DELETE TASKS

    it('Delete a task', () => {
        cy.get('ul.todo-list li.todo-item').first().find('span.remover').click({ force: true })
        cy.get('ul.todo-list li.todo-item').first().find('span.remover').click({ force: true })
     
    })
    

    after(function () {
        cy.resettest()
        })

})