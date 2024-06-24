
describe('GUI Testing', () =>
{
    let uid;
    let name;
    let taskTitle = 'GUI'; // Title for the task in tests

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
        // Setup necessary state via backend before each test
        cy.request('POST', 'http://localhost:5002/tasks/create', { userId: uid, title: taskTitle })
            .then(response =>
            {
                cy.wrap(response.body).as('currentTask');
            });
        cy.visit('http://localhost:3000');
    });



    it('creates a new todo-item via backend and confirms in GUI', () =>
    {
        cy.get('@currentTask').then(task =>
        {
            cy.request('POST', `http://localhost:5002/tasks/${task._id}/todos/create`, { description: 'do gui test' });
        });
        cy.get('.todo-list').should('contain.text', 'do gui test');
    });



    it('checks that the Add button remains disabled if the description is empty', () =>
    {
        cy.get('input[type="text"]').as('todoInput').clear();
        cy.get('input[value="Add"]').should('be.disabled');
    });




    it('toggles a todo item from active to done via backend and confirms in GUI', () =>
    {
        cy.get('@currentTask').then(task =>
        {
            cy.request('POST', `http://localhost:5002/tasks/${task._id}/todos/toggle`, { status: 'active' });
        });
        cy.get('.todo-item').find('span.checker').click();
        cy.get('.todo-item').should('have.css', 'text-decoration', 'line-through solid rgb(49, 46, 46)');
    });




    it('deletes a todo item via backend and confirms deletion in GUI', () =>
    {
        cy.get('@currentTask').then(task =>
        {
            cy.request('DELETE', `http://localhost:5002/tasks/${task._id}/todos/delete`);
        });
        cy.get('.todo-list > li').should('not.exist');
    });




    after(function ()
    {
        // Cleanup by deleting the user created for the test
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5002/users/${uid}`
        });
    });
});

