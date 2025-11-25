import React from "react";
import { COLORS, SHADOWS } from "../Utils/colors";

function Sidebar({ activePage, onChangePage, onLogout }) {
  const items = [
    { key: "dashboard", label: "Dashboard", icon: "📊" },
    { key: "employees", label: "My Employees", icon: "👥" },
    { key: "add-employee", label: "Add Employee", icon: "➕" },
    { key: "remove-employee", label: "Remove Employee", icon: "🗑️" },
    { key: "activity-logs", label: "Activity Logs", icon: "📋" },
    { key: "suspicious", label: "Suspicious Reports", icon: "🚩" },
    { key: "settings", label: "Settings", icon: "⚙️" },
    { key: "profile", label: "Admin Profile", icon: "👤" },
  ];

  return (
    <aside
      style={{
        width: 240,
        background: "white",
        padding: 16,
        borderRight: `1px solid ${COLORS.gray[200]}`,
        boxShadow: SHADOWS.sm,
        display: "flex",
        flexDirection: "column",
        gap: 16,
      }}
    >
      <div style={{ padding: "4px 8px 8px" }}>
        <div
          style={{
            fontSize: 18,
            fontWeight: 700,
            color: COLORS.gray[900],
            marginBottom: 4,
          }}
        >
          Nagster
        </div>
        <div style={{ fontSize: 12, color: COLORS.gray[500] }}>
          Monitoring & Analytics
        </div>
      </div>

      <nav
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          gap: 4,
        }}
      >
        {items.map((item) => {
          const isActive = activePage === item.key;
          return (
            <button
              key={item.key}
              onClick={() => onChangePage(item.key)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                width: "100%",
                padding: "10px 12px",
                borderRadius: 10,
                border: "none",
                background: isActive ? COLORS.primary[50] : "transparent",
                color: isActive ? COLORS.primary[700] : COLORS.gray[700],
                fontSize: 14,
                fontWeight: isActive ? 600 : 500,
                cursor: "pointer",
                textAlign: "left",
              }}
            >
              <span style={{ fontSize: 18 }}>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <button
        onClick={onLogout}
        style={{
          width: "100%",
          padding: "10px 12px",
          borderRadius: 10,
          border: `1px solid ${COLORS.gray[300]}`,
          background: COLORS.gray[50],
          color: COLORS.gray[700],
          fontSize: 14,
          fontWeight: 500,
          cursor: "pointer",
        }}
      >
        Logout
      </button>
    </aside>
  );
}

export default Sidebar;
