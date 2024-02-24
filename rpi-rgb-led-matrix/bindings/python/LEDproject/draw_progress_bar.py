def draw_progress_bar(draw, progress_ratio, pos_x, pos_y, width, height):
    bar_fill_width = int(width * progress_ratio)
    draw.rectangle([(pos_x, pos_y), (pos_x + width, pos_y + height)], fill=(50, 50, 50))  # Draw the background bar
    draw.rectangle([(pos_x, pos_y), (pos_x + bar_fill_width, pos_y + height)], fill=(255, 255, 255))  # Draw the filled bar
