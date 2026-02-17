import { Button, DatePicker, Input } from "antd";
import axios from "axios";
import { useEffect, useState } from "react";

interface Todo {
  id: number;
  user_id: number;
  name: string;
}

export function TodoListPage() {
  const [inputText, setInputText] = useState("");
  const [todoList, setTodoList] = useState([]);

  const loadTodoList = async () => {
    const response = await axios.get("/api/v1/todos");
    setTodoList(response.data);
  };

  useEffect(() => {
    loadTodoList();
  }, []);

  const saveInputText = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputText(event.target.value);
  };

  const addTodo = async () => {
    await axios.post("/api/v1/todos", {
      name: inputText,
    });

    // clear input text after adding
    setInputText("");

    loadTodoList();
  };

  const deleteTodo = async (todoId: number) => {
    await axios.delete(`/api/v1/todos/${todoId}`);
    loadTodoList();
  };

  const handleAddTodoKeyDown = (
    event: React.KeyboardEvent<HTMLInputElement>,
  ) => {
    if (event.key === "Enter") {
      addTodo();
    }
  };
  return (
    <>
      <title>To Do List</title>
      <div className="flex justify-center">
        <div className="min-w-120 p-4">
          <div className="flex gap-2 mb-4">
            <Input
              placeholder="Enter todo name"
              onChange={saveInputText}
              onKeyDown={handleAddTodoKeyDown}
              value={inputText}
              className="w-full flex-1"
            />
            <DatePicker className="w-30" />
            <Button
              color="default"
              variant="solid"
              size="large"
              className="min-w-18.5"
              onClick={addTodo}
            >
              Add
            </Button>
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
    </>
  );
}
