export function getDateFromWeek(weekNumber: number, weekdayName: string): Date {
    const startDate = new Date(new Date().getFullYear(), 0, 1); // Start of the current year
    const dayOfWeek = startDate.getDay(); // Day of the week (0 for Sunday, 1 for Monday, etc.)
    const diff = startDate.getDate() - dayOfWeek + (dayOfWeek == 0 ? -6 : 1); // Adjust to get to the first Monday of the year
    startDate.setDate(diff);
  
    // Calculate the date of the desired week's Monday
    const weekStartDate = new Date(startDate.setDate(startDate.getDate() + (weekNumber - 1) * 7));
  
    // Map of weekday names to their corresponding day index (0 for Sunday, 1 for Monday, etc.)
    const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const dayIndex = weekdays.indexOf(weekdayName);
  
    if (dayIndex === -1) {
      throw new Error("Invalid weekday name");
    }
  
    // Calculate the specific date
    const resultDate = new Date(weekStartDate.setDate(weekStartDate.getDate() + dayIndex));
    return resultDate;
  }