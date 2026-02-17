import { HomePage } from "@/pages/HomePage";
import { SettingsPage } from "@/pages/SettingsPage";
import { TodoListPage } from "@/pages/TodoListPage";
import { Route, Routes } from "react-router-dom";
import { AppLayout } from "./AppLayout";
import LoginPage from "@/pages/LoginPage/ui/LoginPage";
import SignupPage from "@/pages/SignupPage/ui/RegisterPage";

export function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/todo-list" element={<TodoListPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  );
}
