import React, { useEffect, useState } from 'react'
import { Button, Input, DatePicker } from 'antd';
import axios from 'axios';


interface Todo {
  id: number
  user_id: number
  name: string
}

function App() {
  const [inputText, setInputText] = useState('');
  const [todoList, setTodoList] = useState([]);

  const loadTodoList = async () => {
    const response = await axios.get('http://localhost:8000/todo');
    setTodoList(response.data);
  }

  useEffect(() => {
    loadTodoList();
    console.log(todoList);
  }, []);

  const saveInputText = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  }

  const addTodo = async () => {
    await axios.post('http://localhost:8000/todo', {
      name: inputText,
    })
    loadTodoList();
  }

  const deleteTodo = async (todoId: number) => {
    await axios.delete(`http://localhost:8000/todo/${todoId}`);
    loadTodoList();
  }

  const handleAddTodoKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      addTodo();
    }
  }

  return (
    <div className="flex justify-center">
      <div className="min-w-120 p-4">
        <h1 className="flex justify-center m-5 text-2xl font-bold">To Do List</h1>
        <div className="flex gap-2 mb-4">
          <Input placeholder="Enter todo name"
            onChange={saveInputText}
            onKeyDown={handleAddTodoKeyDown}
            className='w-full flex-1'
          />
          <DatePicker className='w-30' />
          <Button 
            color="purple"
            variant="solid"
            size="large"
            className='min-w-18'
            onClick={() => {
              addTodo();
            }}
          >Add</Button>
        </div>
        <div className="flex flex-col gap-2">
          {todoList.map((item: Todo) => {
            return (
              <div key={item.id} className="flex justify-between">
                <div>{item.name}</div>
                <Button 
                  color="danger" 
                  variant="dashed"
                  onClick={() => {
                    deleteTodo(item.id);
                  }}
                >
                  Delete
                </Button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  )
}

export default App
