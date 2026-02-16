import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader
} from "@/components/ui/sidebar"
import { Main, type Item } from "./Main"
import { User } from "./User"
import { ListCheck, Home } from "lucide-react"

const baseItems: Item[] = [
  { icon: Home, title: "Dashboard", path: "/" },
  { icon: ListCheck, title: "Todo", path: "/items" },
]

export function AppSidebar() {
  // TODO: add more options depending on user's privileges
  const items = baseItems

  return (
    <Sidebar>
      <SidebarHeader>
        To Do List
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <User />
      </SidebarFooter>
    </Sidebar>
  )
}