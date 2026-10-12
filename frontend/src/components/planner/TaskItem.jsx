import React from "react";

const TaskItem = ({
  task,
  onComplete,
  onDelete,
}) => {

  return (
    <div
      className={`task-row ${
        task.completed ? "done" : ""
      }`}
    >

      {/* LEFT */}
      <div className="task-left">

        <div
          className={`task-circle ${
            task.completed ? "completed" : ""
          }`}
        >
          {task.completed ? "✓" : ""}
        </div>

        <div>
          <strong>{task.task_name}</strong>

          <p className="muted-text">
            {task.time} • {task.date}
          </p>
        </div>

      </div>

      {/* RIGHT */}
      <div className="task-right">

        {task.completed ? (
          <span className="completed-label">
            Completed
          </span>
        ) : (
          <button
            className="complete-btn"
            onClick={() => onComplete(task)}
          >
            Mark Done
          </button>
        )}

        <button
          className="delete-btn"
          onClick={() => onDelete(task)}
        >
          Delete
        </button>

      </div>

    </div>
  );
};

export default TaskItem;