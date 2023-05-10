describe('user can add, change state and delete todo items', () => {
    let uid
    let name
    let taskId
    let taskTitle
    let doneTodoTitle
    let notDoneTodoTitle
    const beforeHook = () => {
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
                })
            })

        cy.fixture('task.json')
            .then((task) => {
                task["userid"] = uid
                cy.request({
                    method: 'POST',
                    url: `http://localhost:5000/tasks/create`,
                    form: true,
                    body: task
                }).then((response) => {
                    taskId = response.body[0]._id.$oid
                    taskTitle = response.body[0].title
                })
            })
    }

    const afterHook = () => {
        cy.request({
            method: 'DELETE',
            url: `http://localhost:5000/users/${uid}`
        }).then((response) => {
            cy.log(response.body)
        })
    }

    const createTodosHook = () => {
        cy.fixture('todoDone.json')
            .then((todo) => {
                cy.request({
                    method: 'POST',
                    url: `http://localhost:5000/todos/create`,
                    form: true,
                    body: {
                        taskid: taskId,
                        ...todo
                    }
                }).then((response) => {
                    doneTodoTitle = response.body.description
                })
            })

        cy.fixture('todoNotDone.json')
            .then((todo) => {
                cy.request({
                    method: 'POST',
                    url: `http://localhost:5000/todos/create`,
                    form: true,
                    body: {
                        taskid: taskId,
                        ...todo
                    }
                }).then((response) => {
                    notDoneTodoTitle = response.body.description
                })
            })
    }

    const removeTodosHook = () => {
        cy.request({
            method: 'GET',
            url: `http://localhost:5000/tasks/byid/${taskId}`
        }).then((response) => {
            const todoArray = response.body.todos

            for (let todo of todoArray) {
                const id = todo._id.$oid
                cy.request({
                    method: 'DELETE',
                    url: `http://localhost:5000/todos/byid/${id}`
                })
            }
        })
    }

    const loginHook = () => {
        cy.fixture('user.json')
            .then((user) => {
                cy.visit('/')
                cy.contains('div', 'Email Address')
                    .find('input[type=text]')
                    .type(user.email)
                cy.get('form')
                    .submit()

                cy.contains('div', taskTitle)
                    .click()
            })
    }

    before(beforeHook)
    after(afterHook)
    afterEach(removeTodosHook)

    context('add function tests', () => {
        beforeEach(loginHook)
        it('adds todo when title is not empty', () => {
            const newTodoTitle = 'non-empty title'
            cy.get('input[placeholder*="Add a new todo item"]')
                .scrollIntoView()
            cy.get('input[placeholder*="Add a new todo item"]')
                .click()
                .type(newTodoTitle)
            cy.contains('Add')
                .click()
            cy.get('.todo-item')
                .eq(-1)
                .should('contain', newTodoTitle);
        })

        it('add button is disabled when title is empty', () => {
            cy.get('input[placeholder*="Add a new todo item"]')
                .should('have.value', '')
            cy.contains('Add').should('be.disabled')
        })
    })

    context('changing state / delete function tests', () => {
        beforeEach(createTodosHook)
        beforeEach(loginHook)
        it('sets item to done and strikes through the item title when user clicks icon in front of the title',
            () => {
                cy.contains(notDoneTodoTitle).prev()
                    .should('have.class', 'unchecked')
                    .trigger('click')
                cy.contains(notDoneTodoTitle).prev()
                    .should('have.class', 'checked')
                cy.contains(notDoneTodoTitle)
                    .should('have.css', 'text-decoration')
                    .and('include', 'line-through')
            })

        it('sets item to active and removes strikethrough from the item title when user clicks icon ' +
            'in front of the title when item is marked as done', () => {
            cy.contains(doneTodoTitle).prev()
                .should('have.class', 'checked')
                .trigger('click')
            cy.contains(doneTodoTitle).prev()
                .should('have.class', 'unchecked')
            cy.contains(doneTodoTitle)
                .invoke('css', 'text-decoration')
                .should('not.include', 'line-through')
        })

        it('removes item from todo list when user clicks x "behind" the description', () => {
            cy.contains(doneTodoTitle).next()
                .should('contain', '✖')
                .trigger('click')
            cy.get(doneTodoTitle)
                .should('not.exist')
        })
    })
})
