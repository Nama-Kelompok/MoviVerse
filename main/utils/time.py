def format_running_time(running_time):
    if running_time and running_time.isdigit():
        total_minutes = int(running_time)
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        hour_str = "h" if hours == 1 else "h"
        minute_str = "m" if minutes == 1 else "m"
        
        running_time_parts = []
        if hours > 0:
            running_time_parts.append(f"{hours}{hour_str}")
        if minutes > 0:
            running_time_parts.append(f"{minutes}{minute_str}")
        
        return " ".join(running_time_parts)
    else:
        return "Tidak terdapat data waktu tayang"