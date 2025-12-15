import React, {
  useState,
  useEffect,
  useCallback,
  useMemo,
} from "react";

import Sidebar from "../Components/Sidebar";
import StatCard from "../Components/StatCard";
import EmployeeCard from "../Components/EmployeeCard";
import SummaryView from "../Components/SummaryView";
import EmptyState from "../Components/EmptyState";
import LoadingSpinner from "../Components/LoadingSpinner";

import { useApi } from "../Hooks/useApi";
import { COLORS, SHADOWS, primaryGradient } from "../Utils/colors";

import MyEmployees from "./MyEmployees";
import AddEmployee from "./AddEmployee";
import RemoveEmployee from "./RemoveEmployee";
import ActivityLogs from "./ActivityLogs";
import SuspiciousReports from "./SuspiciousReports";
import Settings from "./Settings";
import AdminProfile from "./AdminProfile";

function Dashboard({ user, role, onLogout }) {
  const [activePage, setActivePage] = useState("dashboard");
  const [date, setDate] = useState(
    () => new Date().toISOString().slice(0, 10)
  );
  const [employees, setEmployees] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [summary, setSummary] = useState(null);
  const [activityLogs, setActivityLogs] = useState([]);

  const {
    callApi: fetchOverview,
    loading: loadingList,
    error: listError,
  } = useApi();
  const {
    callApi: fetchSummary,
    loading: loadingSummary,
    error: summaryError,
  } = useApi();
  const {
    callApi: fetchActivity,
    loading: loadingActivity,
    error: activityError,
  } = useApi();

  /* ---------- load overview list ---------- */

  useEffect(() => {
    const loadOverview = async () => {
      try {
        const data = await fetchOverview(`/overview?date_str=${date}`);

        const employeesWithDerived = Array.isArray(data)
          ? data.map((emp) => ({
              ...emp,
              isActive: emp.status === "Active",
            }))
          : [];

        setEmployees(employeesWithDerived);

        if (
          !selectedId ||
          !employeesWithDerived?.find(
            (emp) => emp.employee_id === selectedId
          )
        ) {
          setSelectedId(employeesWithDerived?.[0]?.employee_id || null);
        }
      } catch (err) {
        console.error(err);
        setEmployees([]);
        setSelectedId(null);
      }
    };

    loadOverview();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [date]);

  /* ---------- load summary when selection changes ---------- */

  useEffect(() => {
    if (!selectedId) {
      setSummary(null);
      return;
    }

    const loadSummary = async () => {
      try {
        const data = await fetchSummary(
          `/summary/${selectedId}?date_str=${date}`
        );
        setSummary(data);
      } catch (err) {
        console.error(err);
        setSummary(null);
      }
    };

    loadSummary();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedId, date]);

  /* ---------- load activity logs when Activity Logs page open ---------- */

  useEffect(() => {
    if (activePage !== "activity-logs" || !selectedId) {
      setActivityLogs([]);
      return;
    }

    const loadActivity = async () => {
      try {
        const data = await fetchActivity(
          `/activity/${selectedId}?date_str=${date}`
        );
        setActivityLogs(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error(err);
        setActivityLogs([]);
      }
    };

    loadActivity();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activePage, selectedId, date]);

  /* ---------- derived data ---------- */

  const stats = useMemo(
    () =>
      employees.reduce(
        (acc, emp) => ({
          total: acc.total + 1,
          active: acc.active + (emp.status === "Active" ? 1 : 0),
          suspicious: acc.suspicious + (emp.suspicious_flag_count || 0),
        }),
        { total: 0, active: 0, suspicious: 0 }
      ),
    [employees]
  );

  const selectedEmployee = useMemo(
    () => employees.find((emp) => emp.employee_id === selectedId),
    [employees, selectedId]
  );

  const handleOpenActivityLogs = useCallback((employeeId) => {
    setSelectedId(employeeId);
    setActivePage("activity-logs");
  }, []);

  /* ---------- render ---------- */

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        background: "linear-gradient(135deg, #0f172a 0%, #1e293b 100%)",
      }}
    >
      <Sidebar
        activePage={activePage}
        onChangePage={setActivePage}
        onLogout={onLogout}
        theme="dark"
      />

      <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
        {/* Top bar */}
        <header
          style={{
            background: "rgba(15, 23, 42, 0.8)",
            backdropFilter: "blur(12px)",
            padding: "16px 32px",
            borderBottom: "1px solid rgba(148, 163, 184, 0.2)",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            position: "sticky",
            top: 0,
            zIndex: 50,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div
              style={{
                width: 44,
                height: 44,
                background: "linear-gradient(135deg, #10b981 0%, #059669 100%)",
                borderRadius: 12,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontWeight: "bold",
                fontSize: 22,
                boxShadow: "0 4px 20px rgba(16, 185, 129, 0.3)",
              }}
            >
              N
            </div>
            <div>
              <h2
                style={{
                  margin: 0,
                  fontSize: 22,
                  color: "#f8fafc",
                  fontWeight: 700,
                  letterSpacing: "-0.025em",
                }}
              >
                {activePage === "dashboard"
                  ? "Nagster Dashboard"
                  : activePage === "employees"
                  ? "My Employees"
                  : activePage === "add-employee"
                  ? "Add Employee"
                  : activePage === "remove-employee"
                  ? "Remove Employee"
                  : activePage === "activity-logs"
                  ? "Activity Logs"
                  : activePage === "suspicious"
                  ? "Suspicious Reports"
                  : activePage === "settings"
                  ? "Settings"
                  : "Admin Profile"}
              </h2>
              <p
                style={{
                  margin: 0,
                  fontSize: 13,
                  color: "#94a3b8",
                }}
              >
                {user?.username} •{" "}
                <span style={{ color: "#10b981", fontWeight: 500 }}>
                  {role?.charAt(0).toUpperCase() + role?.slice(1)}
                </span>
              </p>
            </div>
          </div>

          <div style={{ display: "flex", gap: 16, alignItems: "center" }}>
            <div style={{ position: "relative" }}>
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                style={{
                  padding: "12px 16px",
                  borderRadius: 10,
                  border: "1px solid rgba(148, 163, 184, 0.3)",
                  background: "rgba(30, 41, 59, 0.7)",
                  color: "#f1f5f9",
                  fontSize: 14,
                  fontWeight: 500,
                  cursor: "pointer",
                  outline: "none",
                  width: 160,
                  backdropFilter: "blur(8px)",
                }}
              />
            </div>
          </div>
        </header>

        {/* Page content switch */}
        {activePage === "dashboard" && (
          <DashboardHome
            stats={stats}
            employees={employees}
            loadingList={loadingList}
            listError={listError}
            selectedId={selectedId}
            setSelectedId={setSelectedId}
            summary={summary}
            loadingSummary={loadingSummary}
            summaryError={summaryError}
            selectedEmployee={selectedEmployee}
            onViewActivityLogs={handleOpenActivityLogs}
          />
        )}

        {activePage === "employees" && (
          <MyEmployees
            employees={employees}
            loading={loadingList}
            error={listError}
            onSelect={(id) => {
              setSelectedId(id);
              setActivePage("dashboard");
            }}
            onViewActivityLogs={handleOpenActivityLogs}
          />
        )}

        {activePage === "add-employee" && <AddEmployee />}

        {activePage === "remove-employee" && (
          <RemoveEmployee employees={employees} />
        )}

        {activePage === "activity-logs" && (
          <ActivityLogs
            employees={employees}
            selectedId={selectedId}
            setSelectedId={setSelectedId}
            activityLogs={activityLogs}
            loading={loadingActivity}
            error={activityError}
            date={date}
          />
        )}

        {activePage === "suspicious" && (
          <SuspiciousReports employees={employees} />
        )}

        {activePage === "settings" && <Settings />}

        {activePage === "profile" && <AdminProfile user={user} />}
      </div>
    </div>
  );
}

/* ========== dashboard home (main cards + summary) ========== */

function DashboardHome({
  stats,
  employees,
  loadingList,
  listError,
  selectedId,
  setSelectedId,
  summary,
  loadingSummary,
  summaryError,
  selectedEmployee,
  onViewActivityLogs,
}) {
  return (
    <>
      {/* Stats Overview */}
      <div style={{ padding: "32px 32px 0" }}>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
            gap: 24,
            marginBottom: 32,
          }}
        >
          <StatCard 
            label="Total Employees" 
            value={stats.total} 
            icon="👥"
            theme="dark"
          />
          <StatCard
            label="Active Now"
            value={stats.active}
            valueColor="#10b981"
            icon="🟢"
            theme="dark"
          />
          <StatCard
            label="Suspicious Flags"
            value={stats.suspicious}
            valueColor="#ef4444"
            icon="🚩"
            theme="dark"
          />
        </div>
      </div>

      {/* Main layout */}
      <div
        style={{
          padding: "0 32px 32px",
          display: "grid",
          gridTemplateColumns: "minmax(320px, 400px) 1fr",
          gap: 32,
          height: "calc(100vh - 200px)",
        }}
      >
        {/* LEFT: employee list */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.7)",
            backdropFilter: "blur(12px)",
            borderRadius: 20,
            border: "1px solid rgba(148, 163, 184, 0.2)",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
          }}
        >
          <div
            style={{
              padding: "24px 24px 20px",
              borderBottom: "1px solid rgba(148, 163, 184, 0.2)",
              background: "rgba(15, 23, 42, 0.5)",
            }}
          >
            <h3
              style={{
                margin: 0,
                fontSize: 18,
                color: "#f8fafc",
                fontWeight: 600,
              }}
            >
              Employees Overview
            </h3>
            <p
              style={{
                margin: "6px 0 0",
                fontSize: 14,
                color: "#94a3b8",
              }}
            >
              {employees.length} employee
              {employees.length !== 1 ? "s" : ""} found •{" "}
              <span style={{ color: "#10b981", fontWeight: 500 }}>
                {stats.active} active
              </span>
            </p>
          </div>

          <div
            style={{
              flex: 1,
              overflowY: "auto",
              maxHeight: "100%",
            }}
          >
            {loadingList ? (
              <div
                style={{
                  padding: 60,
                  textAlign: "center",
                  color: "#94a3b8",
                  fontSize: 14,
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  gap: 16,
                }}
              >
                <LoadingSpinner />
                Loading employees...
              </div>
            ) : listError ? (
              <div
                style={{
                  padding: 60,
                  textAlign: "center",
                  color: "#ef4444",
                  fontSize: 14,
                }}
              >
                Failed to load employees
              </div>
            ) : employees.length === 0 ? (
              <div
                style={{
                  padding: 60,
                  textAlign: "center",
                  color: "#94a3b8",
                  fontSize: 14,
                }}
              >
                No employees found for this date.
              </div>
            ) : (
              employees.map((emp) => {
                const isSelected = emp.employee_id === selectedId;
                return (
                  <EmployeeCard
                    key={emp.employee_id}
                    employee={emp}
                    isSelected={isSelected}
                    onClick={() => setSelectedId(emp.employee_id)}
                    onViewActivity={onViewActivityLogs}
                    theme="dark"
                  />
                );
              })
            )}
          </div>
        </div>

        {/* RIGHT: summary */}
        <div
          style={{
            background: "rgba(30, 41, 59, 0.7)",
            backdropFilter: "blur(12px)",
            borderRadius: 20,
            border: "1px solid rgba(148, 163, 184, 0.2)",
            display: "flex",
            flexDirection: "column",
            overflow: "hidden",
            boxShadow: "0 8px 32px rgba(0, 0, 0, 0.3)",
          }}
        >
          {!selectedId ? (
            <EmptyState
              icon="👥"
              title="Select an Employee"
              description="Choose an employee from the list to view detailed analytics and activity data."
              theme="dark"
            />
          ) : loadingSummary ? (
            <div
              style={{
                padding: 80,
                textAlign: "center",
                color: "#94a3b8",
                fontSize: 14,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 20,
              }}
            >
              <LoadingSpinner />
              Loading employee details...
            </div>
          ) : summaryError ? (
            <EmptyState
              icon="❌"
              title="Failed to Load Details"
              description="Unable to load employee details. Please try again."
              theme="dark"
            />
          ) : summary ? (
            <SummaryView
              summary={summary}
              employee={selectedEmployee}
              onViewActivity={() =>
                onViewActivityLogs(summary.employee_id)
              }
              theme="dark"
            />
          ) : (
            <EmptyState
              icon="📊"
              title="No Data Available"
              description="No detailed information available for this employee on the selected date."
              theme="dark"
            />
          )}
        </div>
      </div>
    </>
  );
}

export default Dashboard;