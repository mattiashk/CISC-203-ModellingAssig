import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { ScheduleComponent, Inject, Day, Week, WorkWeek, Month, Agenda, DragAndDrop, DragEventArgs, Resize, TimeScaleModel } from '@syncfusion/ej2-react-schedule';
import { DataManager } from '@syncfusion/ej2-data';
import { GridComponent, ColumnsDirective, ColumnDirective, Page } from '@syncfusion/ej2-react-grids';

const StudentTimetable = () => {
  const [others, setOthers] = useState([]);
  const router = useRouter();
  const { studentId, term } = router.query; // Get studentId and term
  const [eventSettings, setEventSettings] = useState<{ dataSource: DataManager }>({ dataSource: new DataManager() });
  const timeScale: TimeScaleModel = { enable: true, interval: 60, slotCount: 2 };

  const onDragStart = (args: DragEventArgs): void => {
    args.scroll = { enable: true, scrollBy: 5, timeDelay: 200 };
    args.navigation = { enable: true, timeDelay: 4000 }
    args.interval = 10;
  }

  useEffect(() => {
    console.log('Fetching events for student:', studentId, 'and term:', term);
    if (studentId && term) {
      fetchData(studentId.toString(), term.toString());
    }
  }, [studentId, term]);

  const fetchData = async (studentId: string, term: string) => {
    try {
      const response = await fetch(`/api/data?studentId=${studentId}&term=${term}`);
      const data = await response.json();
  
      if (response.status !== 200) {
        console.error('Error:', data.message);
        return;
      }
  
      let events = [];
      let others = [];
  
      data.courses.forEach(course => {
        course.dates.forEach(date => {
          if (date.starttime !== "TBA" && date.endtime !== "TBA") {
            events.push({
              Id: course.course + date.starttime,
              Subject: course.course,
              StartTime: new Date(date.starttime),
              EndTime: new Date(date.endtime),
              Location: date.location,
              Description: course.course + ' - ' + date.location
            });
          } else {
            others.push({
              Course: course.course,
              StartTime: date.starttime,
              EndTime: date.endtime,
              Location: date.location
            });
          }
        });
      });
  
      console.log("All Events:", events);
      console.log("Others:", others);
  
      const eventDataManager = new DataManager(events);
      setEventSettings({ dataSource: eventDataManager });
      setOthers(others);
    } catch (error) {
      console.error('Error fetching data:', error);
    }

    console.log(others);
  };

  const handleBackClick = () => {
    router.push('/'); // Redirect to the main index page
  };


  return (
    <div>
      <div>
        <button onClick={handleBackClick} className="bg-blue-500 text-white rounded px-5 py-1 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 mt-5 ml-5 mb-2">
          Back
        </button>
      </div>
      <ScheduleComponent
        selectedDate={new Date()}
        currentView='WorkWeek'
        showHeaderBar={false}
        readonly={true}
        timeScale={timeScale}
        startHour='07:00'
        endHour='22:00'
        eventSettings={{
          dataSource: eventSettings.dataSource,
        }}
        dragStart={onDragStart}
      >
        <Inject services={[WorkWeek, Agenda, DragAndDrop, Resize]} />
      </ScheduleComponent>
      <div>
        {others && others.length > 0 ? (
          <div className="p-10">
            <h2 className="text-4xl font-bold text-center text-black my-4">Other Courses</h2>
            <div className="flex justify-center">
              <GridComponent dataSource={others} allowPaging={true} pageSettings={{ pageSize: 5 }}>
                <ColumnsDirective>
                  <ColumnDirective field='Course' headerText='Course' width='200' textAlign='Center' />
                  <ColumnDirective field='StartTime' headerText='Start Time' width='150' textAlign='Center' />
                  <ColumnDirective field='EndTime' headerText='End Time' width='150' textAlign='Center' />
                  <ColumnDirective field='Location' headerText='Location' width='150' textAlign='Center' />
                </ColumnsDirective>
                <Inject services={[Page]} />
              </GridComponent>
            </div>
          </div>
        ) : (
          <p className="text-black font-bold text-center p-10">No other courses.</p>
        )}
      </div>
    </div>
  );
};

export default StudentTimetable;
