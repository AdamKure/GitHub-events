from datetime import datetime

def get_avg_time_pull(events, repo_id):
    pull_event_list = [event for event in events if event["event_type"]=="PullRequestEvent" and event["repo_id"]==repo_id]
    if len(pull_event_list) < 2:
        raise ValueError("Less than 2 entries")
    
    sorted_pull_list = sorted(pull_event_list, key=lambda x: x["event_time"])  # time increases with increasing index

    first_entry_time = datetime.strptime(sorted_pull_list[0]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
    last_event_time = datetime.strptime(sorted_pull_list[-1]["event_time"], "%Y-%m-%dT%H:%M:%SZ")
    total_time_diff = last_event_time - first_entry_time
    number_of_diffs = len(sorted_pull_list) - 1
    avg_time_diff = total_time_diff / number_of_diffs
    return avg_time_diff
