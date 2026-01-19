@module workflow_engine
@version 1.0.0
@target python

# =============================================================================
# TASK WORKFLOW ENGINE
# A complex example demonstrating NLS capabilities for stress testing
# =============================================================================

# === Enums as Types ===

@type Priority {
  value: string, required
}

@type TaskStatus {
  value: string, required
}

@type WorkflowStatus {
  value: string, required
}

# === Core Entity Types ===

@type User {
  id: string, required
  name: string, required
  email: string, required
  role: string, required
  capacity: number, min: 0, max: 100
  skills: list of string
}

@type TimeEstimate {
  optimistic: number, min: 0
  realistic: number, min: 0
  pessimistic: number, min: 0
}

@type Task {
  id: string, required
  title: string, required
  description: string
  status: TaskStatus, required
  priority: Priority, required
  assignee_id: string, optional
  created_at: number, required
  due_date: number, optional
  completed_at: number, optional
  estimate: TimeEstimate, optional
  actual_hours: number, min: 0
  dependencies: list of string
  tags: list of string
}

@type Workflow {
  id: string, required
  name: string, required
  description: string
  status: WorkflowStatus, required
  owner_id: string, required
  tasks: list of Task
  created_at: number, required
  started_at: number, optional
  completed_at: number, optional
  deadline: number, optional
}

@type Assignment {
  task_id: string, required
  user_id: string, required
  assigned_at: number, required
  assigned_by: string, required
  notes: string, optional
}

@type WorkloadReport {
  user_id: string, required
  total_tasks: number, min: 0
  pending_tasks: number, min: 0
  in_progress_tasks: number, min: 0
  completed_tasks: number, min: 0
  total_estimated_hours: number, min: 0
  utilization_percent: number, min: 0, max: 100
}

@type WorkflowMetrics {
  workflow_id: string, required
  total_tasks: number, min: 0
  completed_tasks: number, min: 0
  blocked_tasks: number, min: 0
  completion_percent: number, min: 0, max: 100
  estimated_completion_date: number, optional
  is_on_track: boolean
  critical_path_length: number, min: 0
}

@type StatusCounts {
  pending: number, min: 0
  in_progress: number, min: 0
  blocked: number, min: 0
  completed: number, min: 0
  cancelled: number, min: 0
}

@type PriorityCounts {
  critical: number, min: 0
  high: number, min: 0
  medium: number, min: 0
  low: number, min: 0
}

@type ReassignmentSuggestion {
  task_id: string, required
  from_user_id: string, required
  to_user_id: string, required
  reason: string
}

# === Invariants ===

@invariant TimeEstimate {
  optimistic <= realistic
  realistic <= pessimistic
  pessimistic > 0
}

@invariant Task {
  actual_hours >= 0
}

@invariant WorkloadReport {
  utilization_percent >= 0
  utilization_percent <= 100
}

# =============================================================================
# PRIORITY FUNCTIONS
# =============================================================================

[priority-to-weight]
PURPOSE: Convert priority to numeric weight for sorting.
INPUTS:
  - priority: Priority
LOGIC:
  1. Map critical to 4, high to 3, medium to 2, low to 1 -> weight
RETURNS: weight based on priority value

[compare-priorities]
PURPOSE: Compare two priorities, returning -1, 0, or 1.
INPUTS:
  - a: Priority
  - b: Priority
LOGIC:
  1. Get weight of a -> weight_a
  2. Get weight of b -> weight_b
  3. Calculate difference -> diff
RETURNS: 1 if weight_a > weight_b, -1 if weight_a < weight_b, else 0
DEPENDS: [priority-to-weight]

[get-highest-priority]
PURPOSE: Get the highest priority from a list of tasks.
INPUTS:
  - tasks: list of Task
GUARDS:
  - len(tasks) > 0 -> ValueError("Cannot get priority from empty list")
LOGIC:
  1. Extract priorities from all tasks -> priorities
  2. Find maximum by weight -> highest
RETURNS: highest priority
DEPENDS: [priority-to-weight]

# =============================================================================
# TIME ESTIMATION FUNCTIONS
# =============================================================================

[calculate-pert-estimate]
PURPOSE: Calculate PERT estimate using formula (O + 4M + P) / 6.
INPUTS:
  - estimate: TimeEstimate
GUARDS:
  - estimate.optimistic <= estimate.realistic -> ValueError("Optimistic must be <= realistic")
  - estimate.realistic <= estimate.pessimistic -> ValueError("Realistic must be <= pessimistic")
LOGIC:
  1. Apply PERT formula -> pert
RETURNS: (estimate.optimistic + 4 * estimate.realistic + estimate.pessimistic) / 6

[calculate-estimate-variance]
PURPOSE: Calculate variance in time estimate for risk assessment.
INPUTS:
  - estimate: TimeEstimate
LOGIC:
  1. Calculate range -> range_val
  2. Divide by 6 and square -> variance
RETURNS: ((estimate.pessimistic - estimate.optimistic) / 6) ** 2

[calculate-estimate-std-dev]
PURPOSE: Calculate standard deviation of time estimate.
INPUTS:
  - estimate: TimeEstimate
LOGIC:
  1. Calculate variance -> var
  2. Take square root -> std_dev
RETURNS: sqrt(variance)
DEPENDS: [calculate-estimate-variance]

[sum-estimates]
PURPOSE: Sum multiple time estimates into one combined estimate.
INPUTS:
  - estimates: list of TimeEstimate
GUARDS:
  - len(estimates) > 0 -> ValueError("Cannot sum empty list of estimates")
LOGIC:
  1. Sum all optimistic values -> total_opt
  2. Sum all realistic values -> total_real
  3. Sum all pessimistic values -> total_pess
RETURNS: TimeEstimate with summed values

[average-estimate]
PURPOSE: Calculate average of multiple time estimates.
INPUTS:
  - estimates: list of TimeEstimate
GUARDS:
  - len(estimates) > 0 -> ValueError("Cannot average empty list")
LOGIC:
  1. Sum all estimates -> total
  2. Divide each component by count -> avg
RETURNS: average TimeEstimate
DEPENDS: [sum-estimates]

# =============================================================================
# TASK STATUS FUNCTIONS
# =============================================================================

[is-task-actionable]
PURPOSE: Check if a task can be worked on (not blocked or completed).
INPUTS:
  - task: Task
LOGIC:
  1. Check status is pending or in_progress -> actionable
RETURNS: task.status.value in ["pending", "in_progress"]

[is-task-terminal]
PURPOSE: Check if a task is in a terminal state.
INPUTS:
  - task: Task
RETURNS: task.status.value in ["completed", "cancelled"]

[is-task-blocked]
PURPOSE: Check if a task has blocked status.
INPUTS:
  - task: Task
RETURNS: task.status.value == "blocked"

[count-tasks-by-status]
PURPOSE: Count tasks matching a specific status.
INPUTS:
  - tasks: list of Task
  - status_value: string
LOGIC:
  1. Filter tasks to matching status -> matching
  2. Count matching tasks -> count
RETURNS: count of matching tasks

[get-status-counts]
PURPOSE: Get counts of tasks by each status.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Count pending tasks -> pending
  2. Count in_progress tasks -> in_progress
  3. Count blocked tasks -> blocked
  4. Count completed tasks -> completed
  5. Count cancelled tasks -> cancelled
RETURNS: StatusCounts with all counts
DEPENDS: [count-tasks-by-status]

# =============================================================================
# DEPENDENCY MANAGEMENT
# =============================================================================

[get-task-by-id]
PURPOSE: Find a task by its ID.
INPUTS:
  - tasks: list of Task
  - task_id: string
LOGIC:
  1. Search for task with matching ID -> found
RETURNS: found task or None

[get-blocking-tasks]
PURPOSE: Get list of incomplete tasks that block a given task.
INPUTS:
  - task: Task
  - all_tasks: list of Task
LOGIC:
  1. Get task IDs from dependencies -> dep_ids
  2. Find tasks matching those IDs -> deps
  3. Filter to non-terminal tasks -> blocking
RETURNS: list of blocking tasks
DEPENDS: [get-task-by-id], [is-task-terminal]

[has-unmet-dependencies]
PURPOSE: Check if a task is blocked by incomplete dependencies.
INPUTS:
  - task: Task
  - all_tasks: list of Task
LOGIC:
  1. Get blocking tasks -> blockers
  2. Check if any blockers exist -> blocked
RETURNS: len(blockers) > 0
DEPENDS: [get-blocking-tasks]

[get-ready-tasks]
PURPOSE: Get all tasks that are ready to be worked on.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to actionable tasks -> actionable
  2. Filter to those not blocked -> ready
RETURNS: list of ready tasks
DEPENDS: [is-task-actionable], [has-unmet-dependencies]

[get-dependency-depth]
PURPOSE: Calculate the maximum dependency chain depth for a task.
INPUTS:
  - task: Task
  - all_tasks: list of Task
LOGIC:
  1. Get direct dependencies -> deps
  2. Recursively calculate depth of each -> depths
  3. Return max depth plus 1 -> total_depth
RETURNS: maximum dependency depth
DEPENDS: [get-task-by-id]

[detect-circular-dependencies]
PURPOSE: Detect if there are circular dependencies in task list.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Build adjacency list -> adj
  2. Track visited and recursion stack -> visited, rec_stack
  3. DFS from each unvisited node -> has_cycle
RETURNS: True if circular dependency exists, False otherwise

[topological-sort-tasks]
PURPOSE: Sort tasks by dependency order.
INPUTS:
  - tasks: list of Task
GUARDS:
  - not detect_circular_dependencies(tasks) -> ValueError("Circular dependency detected")
LOGIC:
  1. Build dependency graph -> graph
  2. Find tasks with no dependencies -> roots
  3. Process queue, adding tasks when deps satisfied -> sorted_list
RETURNS: topologically sorted list of tasks
DEPENDS: [detect-circular-dependencies]

# =============================================================================
# ASSIGNMENT FUNCTIONS
# =============================================================================

[create-assignment]
PURPOSE: Create a new assignment record.
INPUTS:
  - task_id: string
  - user_id: string
  - assigner_id: string
  - timestamp: number
  - notes: string, optional
LOGIC:
  1. Build assignment record -> assignment
RETURNS: new Assignment

[assign-task-to-user]
PURPOSE: Assign a task to a user.
INPUTS:
  - task: Task
  - user: User
  - assigner_id: string
  - timestamp: number
GUARDS:
  - is_task_actionable(task) -> ValueError("Cannot assign terminal task")
  - user.capacity > 0 -> ValueError("User has no available capacity")
LOGIC:
  1. Create assignment record -> assignment
  2. Update task with assignee -> updated_task
RETURNS: tuple of updated_task and assignment
DEPENDS: [is-task-actionable], [create-assignment]

[unassign-task]
PURPOSE: Remove assignment from a task.
INPUTS:
  - task: Task
GUARDS:
  - task.assignee_id != None -> ValueError("Task is not assigned")
LOGIC:
  1. Clear assignee_id from task -> updated
RETURNS: updated task with no assignee

[reassign-task]
PURPOSE: Reassign a task from one user to another.
INPUTS:
  - task: Task
  - new_user: User
  - assigner_id: string
  - timestamp: number
LOGIC:
  1. Unassign current user -> unassigned
  2. Assign to new user -> reassigned
RETURNS: reassigned task and new assignment
DEPENDS: [unassign-task], [assign-task-to-user]

[get-user-tasks]
PURPOSE: Get all tasks assigned to a user.
INPUTS:
  - tasks: list of Task
  - user_id: string
LOGIC:
  1. Filter tasks to user -> user_tasks
RETURNS: list of tasks assigned to user

# =============================================================================
# WORKLOAD CALCULATION
# =============================================================================

[calculate-task-hours]
PURPOSE: Calculate estimated hours for a single task.
INPUTS:
  - task: Task
LOGIC:
  1. Check if task has estimate -> has_est
  2. Calculate PERT if has estimate, else default -> hours
RETURNS: estimated hours for task
DEPENDS: [calculate-pert-estimate]

[calculate-total-hours]
PURPOSE: Calculate total estimated hours for a list of tasks.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Calculate hours for each task -> hours_list
  2. Sum all hours -> total
RETURNS: total estimated hours
DEPENDS: [calculate-task-hours]

[calculate-user-workload]
PURPOSE: Calculate workload report for a user.
INPUTS:
  - user: User
  - tasks: list of Task
LOGIC:
  1. Filter tasks assigned to user -> user_tasks
  2. Count by status -> counts
  3. Sum estimates for incomplete tasks -> estimated_hours
  4. Calculate utilization -> util_percent
RETURNS: WorkloadReport for the user
DEPENDS: [get-user-tasks], [get-status-counts], [calculate-total-hours]

[calculate-team-workload]
PURPOSE: Calculate combined workload for a team.
INPUTS:
  - users: list of User
  - tasks: list of Task
LOGIC:
  1. Calculate workload for each user -> workloads
  2. Aggregate totals -> team_totals
RETURNS: aggregated workload report
DEPENDS: [calculate-user-workload]

[find-least-loaded-user]
PURPOSE: Find user with lowest current workload.
INPUTS:
  - users: list of User
  - tasks: list of Task
GUARDS:
  - len(users) > 0 -> ValueError("No users provided")
LOGIC:
  1. Calculate workload for each user -> workloads
  2. Find minimum utilization -> min_load
  3. Return user with minimum -> least_loaded
RETURNS: user with lowest workload
DEPENDS: [calculate-user-workload]

[find-most-loaded-user]
PURPOSE: Find user with highest current workload.
INPUTS:
  - users: list of User
  - tasks: list of Task
GUARDS:
  - len(users) > 0 -> ValueError("No users provided")
LOGIC:
  1. Calculate workload for each user -> workloads
  2. Find maximum utilization -> max_load
  3. Return user with maximum -> most_loaded
RETURNS: user with highest workload
DEPENDS: [calculate-user-workload]

[get-overloaded-users]
PURPOSE: Find users whose utilization exceeds threshold.
INPUTS:
  - users: list of User
  - tasks: list of Task
  - threshold: number
LOGIC:
  1. Calculate workload for each user -> workloads
  2. Filter to those over threshold -> overloaded
RETURNS: list of overloaded users
DEPENDS: [calculate-user-workload]

[balance-workload]
PURPOSE: Suggest task reassignments to balance workload.
INPUTS:
  - users: list of User
  - tasks: list of Task
  - threshold: number
LOGIC:
  1. Calculate workloads for all users -> workloads
  2. Find overloaded and underloaded users -> over, under
  3. Generate reassignment suggestions -> suggestions
RETURNS: list of ReassignmentSuggestion
DEPENDS: [calculate-user-workload], [get-overloaded-users]

# =============================================================================
# WORKFLOW METRICS
# =============================================================================

[calculate-workflow-progress]
PURPOSE: Calculate completion percentage of a workflow.
INPUTS:
  - workflow: Workflow
GUARDS:
  - len(workflow.tasks) > 0 -> ValueError("Workflow has no tasks")
LOGIC:
  1. Count completed tasks -> completed
  2. Count total tasks -> total
  3. Calculate percentage -> percent
RETURNS: (completed / total) * 100

[calculate-remaining-work]
PURPOSE: Calculate total remaining work in hours.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to incomplete tasks -> incomplete
  2. Sum PERT estimates -> total_hours
RETURNS: total remaining hours
DEPENDS: [is-task-terminal], [calculate-task-hours]

[calculate-completed-work]
PURPOSE: Calculate total completed work in hours.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to completed tasks -> completed
  2. Sum actual hours -> total_hours
RETURNS: total completed hours
DEPENDS: [is-task-terminal]

[calculate-velocity]
PURPOSE: Calculate team velocity in hours per day.
INPUTS:
  - tasks: list of Task
  - start_time: number
  - end_time: number
GUARDS:
  - end_time > start_time -> ValueError("End time must be after start time")
LOGIC:
  1. Calculate completed work in period -> completed_hours
  2. Calculate days elapsed -> days
  3. Divide hours by days -> velocity
RETURNS: velocity in hours per day
DEPENDS: [calculate-completed-work]

[estimate-completion-date]
PURPOSE: Estimate when workflow will complete.
INPUTS:
  - workflow: Workflow
  - current_time: number
  - velocity_hours_per_day: number
GUARDS:
  - velocity_hours_per_day > 0 -> ValueError("Velocity must be positive")
LOGIC:
  1. Calculate remaining work -> remaining_hours
  2. Calculate days needed -> days_needed
  3. Add to current time -> completion_date
RETURNS: estimated completion timestamp
DEPENDS: [calculate-remaining-work]

[is-workflow-on-track]
PURPOSE: Check if workflow is on track to meet deadline.
INPUTS:
  - workflow: Workflow
  - current_time: number
  - velocity_hours_per_day: number
LOGIC:
  1. Estimate completion date -> est_completion
  2. Compare to deadline -> on_track
RETURNS: True if on track, False otherwise
DEPENDS: [estimate-completion-date]

[calculate-critical-path-length]
PURPOSE: Calculate the length of the critical path in hours.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Sort tasks topologically -> sorted_tasks
  2. Calculate longest path through graph -> critical_path
  3. Sum estimates along path -> total_hours
RETURNS: critical path length in hours
DEPENDS: [topological-sort-tasks], [calculate-task-hours]

[calculate-workflow-metrics]
PURPOSE: Calculate comprehensive metrics for a workflow.
INPUTS:
  - workflow: Workflow
  - current_time: number
  - velocity_hours_per_day: number
LOGIC:
  1. Count tasks by status -> counts
  2. Calculate progress percentage -> progress
  3. Estimate completion date -> est_completion
  4. Determine if on track -> on_track
  5. Calculate critical path -> critical_length
RETURNS: WorkflowMetrics
DEPENDS: [calculate-workflow-progress], [calculate-critical-path-length], [estimate-completion-date], [is-workflow-on-track], [get-status-counts]

# =============================================================================
# WORKFLOW LIFECYCLE
# =============================================================================

[create-workflow]
PURPOSE: Create a new workflow in draft status.
INPUTS:
  - id: string
  - name: string
  - owner_id: string
  - timestamp: number
LOGIC:
  1. Create workflow with draft status -> workflow
RETURNS: new Workflow in draft status

[add-task-to-workflow]
PURPOSE: Add a task to a workflow.
INPUTS:
  - workflow: Workflow
  - task: Task
GUARDS:
  - workflow.status.value == "draft" -> ValueError("Can only add tasks to draft workflows")
LOGIC:
  1. Append task to workflow tasks -> updated
RETURNS: updated workflow

[remove-task-from-workflow]
PURPOSE: Remove a task from a workflow.
INPUTS:
  - workflow: Workflow
  - task_id: string
GUARDS:
  - workflow.status.value == "draft" -> ValueError("Can only remove tasks from draft workflows")
LOGIC:
  1. Filter out task with ID -> updated
RETURNS: updated workflow
DEPENDS: [get-task-by-id]

[activate-workflow]
PURPOSE: Activate a draft workflow.
INPUTS:
  - workflow: Workflow
  - timestamp: number
GUARDS:
  - workflow.status.value == "draft" -> ValueError("Can only activate draft workflows")
  - len(workflow.tasks) > 0 -> ValueError("Cannot activate empty workflow")
  - not detect_circular_dependencies(workflow.tasks) -> ValueError("Workflow has circular dependencies")
LOGIC:
  1. Update status to active -> updated
  2. Set started_at timestamp -> final
RETURNS: activated workflow
DEPENDS: [detect-circular-dependencies]

[pause-workflow]
PURPOSE: Pause an active workflow.
INPUTS:
  - workflow: Workflow
GUARDS:
  - workflow.status.value == "active" -> ValueError("Can only pause active workflows")
LOGIC:
  1. Update status to paused -> updated
RETURNS: paused workflow

[resume-workflow]
PURPOSE: Resume a paused workflow.
INPUTS:
  - workflow: Workflow
GUARDS:
  - workflow.status.value == "paused" -> ValueError("Can only resume paused workflows")
LOGIC:
  1. Update status to active -> updated
RETURNS: resumed workflow

[all-tasks-terminal]
PURPOSE: Check if all tasks in a list are terminal.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Check each task is terminal -> all_done
RETURNS: all tasks are completed or cancelled
DEPENDS: [is-task-terminal]

[complete-workflow]
PURPOSE: Mark a workflow as completed.
INPUTS:
  - workflow: Workflow
  - timestamp: number
GUARDS:
  - workflow.status.value == "active" -> ValueError("Can only complete active workflows")
  - all_tasks_terminal(workflow.tasks) -> ValueError("Cannot complete workflow with pending tasks")
LOGIC:
  1. Update status to completed -> updated
  2. Set completed_at timestamp -> final
RETURNS: completed workflow
DEPENDS: [all-tasks-terminal]

[archive-workflow]
PURPOSE: Archive a completed workflow.
INPUTS:
  - workflow: Workflow
GUARDS:
  - workflow.status.value == "completed" -> ValueError("Can only archive completed workflows")
LOGIC:
  1. Update status to archived -> updated
RETURNS: archived workflow

# =============================================================================
# TASK FILTERING AND SEARCH
# =============================================================================

[filter-tasks-by-status]
PURPOSE: Filter tasks to those matching a status.
INPUTS:
  - tasks: list of Task
  - status: TaskStatus
RETURNS: tasks matching status

[filter-tasks-by-priority]
PURPOSE: Filter tasks to those matching a priority.
INPUTS:
  - tasks: list of Task
  - priority: Priority
RETURNS: tasks matching priority

[filter-tasks-by-assignee]
PURPOSE: Filter tasks to those assigned to a user.
INPUTS:
  - tasks: list of Task
  - user_id: string
RETURNS: tasks assigned to user

[filter-unassigned-tasks]
PURPOSE: Filter to tasks with no assignee.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to tasks where assignee_id is None -> unassigned
RETURNS: unassigned tasks

[filter-overdue-tasks]
PURPOSE: Filter tasks that are past their due date.
INPUTS:
  - tasks: list of Task
  - current_time: number
LOGIC:
  1. Filter to tasks with due_date set -> with_due
  2. Filter to non-terminal past due -> overdue
RETURNS: list of overdue tasks
DEPENDS: [is-task-terminal]

[filter-tasks-due-soon]
PURPOSE: Filter tasks due within a time window.
INPUTS:
  - tasks: list of Task
  - current_time: number
  - window_hours: number
LOGIC:
  1. Calculate deadline threshold -> threshold
  2. Filter tasks due before threshold -> due_soon
RETURNS: tasks due soon
DEPENDS: [is-task-terminal]

[search-tasks-by-tag]
PURPOSE: Find tasks that have a specific tag.
INPUTS:
  - tasks: list of Task
  - tag: string
RETURNS: tasks with matching tag

[search-tasks-by-title]
PURPOSE: Find tasks with title containing search term.
INPUTS:
  - tasks: list of Task
  - search_term: string
LOGIC:
  1. Filter tasks where title contains term -> matching
RETURNS: matching tasks

[sort-tasks-by-priority]
PURPOSE: Sort tasks by priority highest first.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Sort using priority weight as key -> sorted_tasks
RETURNS: sorted list of tasks
DEPENDS: [priority-to-weight]

[sort-tasks-by-due-date]
PURPOSE: Sort tasks by due date earliest first.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Separate tasks with and without due dates -> with_due, no_due
  2. Sort tasks with due dates -> sorted_due
  3. Append tasks without due dates -> combined
RETURNS: sorted list of tasks

[sort-tasks-by-created-date]
PURPOSE: Sort tasks by creation date oldest first.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Sort by created_at ascending -> sorted_tasks
RETURNS: sorted list of tasks

# =============================================================================
# REPORTING
# =============================================================================

[generate-status-summary]
PURPOSE: Generate a summary of task counts by status.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Get status counts -> counts
RETURNS: StatusCounts
DEPENDS: [get-status-counts]

[generate-priority-summary]
PURPOSE: Generate a summary of task counts by priority.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Count critical tasks -> critical
  2. Count high tasks -> high
  3. Count medium tasks -> medium
  4. Count low tasks -> low
RETURNS: PriorityCounts

[calculate-average-completion-time]
PURPOSE: Calculate average time to complete tasks.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to completed tasks with timestamps -> completed
  2. Calculate duration for each -> durations
  3. Average the durations -> avg_time
RETURNS: average completion time in hours

[calculate-estimation-accuracy]
PURPOSE: Calculate how accurate estimates were vs actual.
INPUTS:
  - tasks: list of Task
LOGIC:
  1. Filter to tasks with estimates and actuals -> with_data
  2. Calculate estimate vs actual ratio for each -> ratios
  3. Average the ratios -> accuracy
RETURNS: accuracy percentage
DEPENDS: [calculate-pert-estimate]

[generate-user-performance-report]
PURPOSE: Generate performance metrics for a user.
INPUTS:
  - user: User
  - tasks: list of Task
  - period_start: number
  - period_end: number
LOGIC:
  1. Get user tasks in period -> user_tasks
  2. Calculate completed count -> completed
  3. Calculate average completion time -> avg_time
  4. Calculate estimation accuracy -> accuracy
RETURNS: performance report for user
DEPENDS: [get-user-tasks], [calculate-average-completion-time], [calculate-estimation-accuracy]

[generate-workflow-summary]
PURPOSE: Generate executive summary of workflow status.
INPUTS:
  - workflow: Workflow
  - current_time: number
  - velocity_hours_per_day: number
LOGIC:
  1. Calculate metrics -> metrics
  2. Generate summary text -> summary
RETURNS: workflow summary
DEPENDS: [calculate-workflow-metrics]

# =============================================================================
# TESTS
# =============================================================================

@test [priority-to-weight] {
  priority_to_weight(Priority(value="critical")) == 4
  priority_to_weight(Priority(value="high")) == 3
  priority_to_weight(Priority(value="medium")) == 2
  priority_to_weight(Priority(value="low")) == 1
}

@test [compare-priorities] {
  compare_priorities(Priority(value="high"), Priority(value="low")) == 1
  compare_priorities(Priority(value="low"), Priority(value="high")) == -1
  compare_priorities(Priority(value="medium"), Priority(value="medium")) == 0
}

@test [calculate-pert-estimate] {
  calculate_pert_estimate(TimeEstimate(optimistic=1, realistic=2, pessimistic=3)) == 2.0
  calculate_pert_estimate(TimeEstimate(optimistic=2, realistic=4, pessimistic=12)) == 5.0
  calculate_pert_estimate(TimeEstimate(optimistic=1, realistic=1, pessimistic=1)) == 1.0
}

@test [calculate-estimate-variance] {
  calculate_estimate_variance(TimeEstimate(optimistic=1, realistic=2, pessimistic=7)) == 1.0
  calculate_estimate_variance(TimeEstimate(optimistic=2, realistic=2, pessimistic=2)) == 0.0
}

@test [is-task-actionable] {
  is_task_actionable(Task(id="1", title="Test", status=TaskStatus(value="pending"), priority=Priority(value="low"), created_at=0)) == True
  is_task_actionable(Task(id="1", title="Test", status=TaskStatus(value="completed"), priority=Priority(value="low"), created_at=0)) == False
}

@test [is-task-terminal] {
  is_task_terminal(Task(id="1", title="Test", status=TaskStatus(value="completed"), priority=Priority(value="low"), created_at=0)) == True
  is_task_terminal(Task(id="1", title="Test", status=TaskStatus(value="cancelled"), priority=Priority(value="low"), created_at=0)) == True
  is_task_terminal(Task(id="1", title="Test", status=TaskStatus(value="pending"), priority=Priority(value="low"), created_at=0)) == False
}

# =============================================================================
# PROPERTY-BASED TESTS
# =============================================================================

@property [priority-to-weight] {
  priority_to_weight(p) >= 0
  priority_to_weight(p) <= 4
}

@property [calculate-pert-estimate] {
  forall e: TimeEstimate -> calculate_pert_estimate(e) >= e.optimistic
  forall e: TimeEstimate -> calculate_pert_estimate(e) <= e.pessimistic
}

@property [compare-priorities] {
  compare_priorities(a, a) == 0
  compare_priorities(a, b) == -compare_priorities(b, a)
}

@property [calculate-workflow-progress] {
  forall w: Workflow -> calculate_workflow_progress(w) >= 0
  forall w: Workflow -> calculate_workflow_progress(w) <= 100
}

@property [calculate-remaining-work] {
  forall tasks: list of Task -> calculate_remaining_work(tasks) >= 0
}
