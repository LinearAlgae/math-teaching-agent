import { MessageRole } from "../types";

interface RoleSelectorProps {
  role: MessageRole;
  onRoleChange: (role: MessageRole) => void;
}

export function RoleSelector({ role, onRoleChange }: RoleSelectorProps) {
  return (
    <div className="role-selector">
      <button
        className={`role-button ${role === "student" ? "active" : ""}`}
        onClick={() => onRoleChange("student")}
      >
        学生
      </button>
      <button
        className={`role-button ${role === "teacher" ? "active" : ""}`}
        onClick={() => onRoleChange("teacher")}
      >
        教师
      </button>
    </div>
  );
}