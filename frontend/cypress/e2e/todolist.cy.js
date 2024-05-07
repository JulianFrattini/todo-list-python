
describe('GUI Testing', () =>
{
    let uid;
    let name;
    let taskTitle = 'GUI'; // Title for the task in tests
    let todo1 = 'do gui test'; // Description for the first todo item

    before(function ()
    {
        // Initialize by creating a user based on fixture data
        cy.fixture('user.json').then((user) =>
        {
            cy.request({
                method: 'POST',
                url: 'http://localhost:5002/users/create',
                form: true,
                body: user
            }).then((response) =>
            {
                uid = response.body._id.$oid;
                name = `${user.firstName} ${user.lastName}`; // Concatenate name for display checks
            });
        });
    });

    beforeEach(function ()
    {
        // Visit main page before each test
        cy.visit('http://localhost:3000');
    });

    it('validates the login screen', () =>
    {
        // Ensure the login screen is correctly displayed
        cy.get('h1').should('contain.text', 'Login');
    });



    //----------------R8UC1--------------//

    it(' creating a new todo-item', () =>
    {
        // Test the creation of a new todo item
        cy.contains('div', 'Email Address').find('input[type=text]').type('mon.doe@gmail.com');
        cy.get('form').submit();
        cy.get('h1').should('contain.text', 'Your tasks, ' + name);

        cy.get('.inputwrapper #title').type(taskTitle);
        cy.get('form').submit();

        cy.contains('div', taskTitle).should('contain.text', taskTitle).click();
        cy.get('.popup-inner').find('form').should('have.class', 'inline-form')
            .find('input[type="text"]').as('todoInput').should('exist').and('have.value', '');

        cy.get('.popup-inner').find('.todo-list').find('input[value="Add"]').as('addButton')
            .should('be.disabled').then(($btn) =>
            {
                cy.get('@todoInput').type(todo1, { force: true }).should('not.have.value', '');
                cy.get('@addButton').should('be.enabled').click();
            });

        cy.get('.todo-list').children('.todo-item').last().should('contain.text', todo1);
    });


    //----------------R8UC2--------------//
    it('toggles an active  to done', () =>
    {
        // Test the toggling of an active 'done' status
        cy.contains('div', 'Email Address').find('input[type=text]').type('mon.doe@gmail.com{enter}');
        cy.get('.container-element').find('a').first().click();

        cy.get('.todo-list').first().find('.todo-item').first().as('todoItem')
            .find('span.editable').as('todoName')
            .should('not.have.css', 'text-decoration', 'line-through');

        cy.get('@todoItem').find('span.checker').click();
        cy.get('@todoName').should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)');
    });


    //----------------R8UC2--------------//
    it('reverts a done to active', () =>
    {
        // Test reverting done active status
        cy.contains('div', 'Email Address').find('input[type=text]').type('mon.doe@gmail.com{enter}');
        cy.get('.container-element').find('a').first().click();

        cy.get('.todo-list').first().find('.todo-item').first().as('todoItem')
            .find('span.editable').as('todoName')
            .invoke('css', 'text-decoration').should('include', 'line-through');

        cy.get('@todoItem').find('span.checker').click();
        cy.get('@todoName').should('not.have.css', 'text-decoration', 'line-through');
    });


    //----------------R8UC3--------------//
    it('deletes a todo item', () =>
    {
        // Test the deletion of a todo item
        cy.contains('div', 'Email Address').find('input[type=text]').type('mon.doe@gmail.com{enter}');
        cy.get('.container-element').find('a').first().click();

        cy.get('ul').should('have.class', 'todo-list');
        cy.get('.todo-list > li').first().find('.remover').click();
        cy.wait(500); // Wait for 500 ms
        cy.get('.todo-list > li').should('not.exist');

    });

    after(function ()
    {
        //  delete the user created for the test
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5002/users/${uid}`
        }).then((response) =>
        {
            cy.log(response.body);
        });
    });
});

