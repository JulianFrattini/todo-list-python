module.exports = {
    convertTask: function (taskobj) {
        let todolist = []
        let done = true;

        for (const todo of taskobj.todos) {
            if(done && !todo.done) {
                done = false;
            }

            todolist.push({
                _id: todo['_id']['$oid'],
                description: todo.description,
                done: todo.done
            })
        }

        let task = {
            _id: taskobj['_id']['$oid'],
            title: taskobj.title,
            description: taskobj.description,
            url: taskobj.video.url,
            todos: todolist,
            done: done
        }

        return task;
    }
}