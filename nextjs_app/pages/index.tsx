import React, { useEffect, useState, useRef  } from 'react';
import { GridComponent, ColumnsDirective, ColumnDirective, Inject, Page } from '@syncfusion/ej2-react-grids';
import { useRouter } from 'next/router';
import Image from "next/image"
import { DropDownListComponent } from '@syncfusion/ej2-react-dropdowns';
import { ToastComponent} from '@syncfusion/ej2-react-notifications';

const IndexPage = () => {
  const [data, setData] = useState([]);
  const router = useRouter();
  const [selectedTestCase, setSelectedTestCase] = useState('0');

  const toastRef = useRef(null);

  const showToast = (type, title, content) => {
    if (toastRef.current) {
      toastRef.current.show({
        title: title,
        content: content,
        cssClass: `e-toast-${type}`,
        icon: type,
      });
    }
  };

  const onClose = () => {
    document.getElementById('toast').style.backgroundColor = 'white';
  };
  

  const testData: { [key: string]: Object }[] = [
    { Id: '0', Name: 'Test Case 0' },
    { Id: '1', Name: 'Test Case 1' },
    { Id: '2', Name: 'Test Case 2' }
  ];
  const fields: object = { text: 'Name', value: 'Id' };

  const handleTestCaseChange = (e) => {
    setSelectedTestCase(e.value);
  };

  const handleGenerateDataClick = async () => {
    try {
      const response = await fetch('http://localhost:5000/parse-test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ test_case: selectedTestCase })
      });

      if (response.ok) {
        showToast('success', 'Success!', 'Your request has been sent successfully.');
        setTimeout(() => {window.location.reload();}, 3000);
      } else {
        showToast('error', 'Error!', 'A problem has occurred while submitting your request.');
        setTimeout(() => {window.location.reload();}, 3000);
      }
    } catch (error) {
      showToast('error', 'Error!', error.message);
    }
  };

  useEffect(() => {
    fetch('/api/student-overview')
      .then(response => response.json())
      .then(data => setData(data));
  }, []);

  const redirectToTimetable = (studentName, term) => {
    router.push(`/timetable/${studentName}/${term}`);
  };


  return (
    <div>
      <div id='#toast_target' className="bg-white text-center p-8">
          <ToastComponent id='toast' className='toast-container' target="#toast_target" ref={toastRef} position={{ X: 'Right', Y: 'Top' } } created={showToast} close={onClose}/>
        <h1 className="text-3xl font-bold uppercase text-gray-800">SCHEDULE SENSEI</h1>
        <Image src="/logo.png" alt="Schedule Sensei" width={200} height={200} className="mx-auto my-12" />
        {data && data.length > 0 ? (
          <div className="mx-auto w-1/2 p-8">
            <GridComponent dataSource={data} allowPaging={true} pageSettings={{ pageSize: 10 }}>
              <ColumnsDirective>
                <ColumnDirective field='Name' headerText='Student Name' width='200' textAlign='Left' />
                <ColumnDirective field='Fall' headerText='Fall Term' width='150' textAlign='Center' template={(props) =>
                  props.Fall ? <button className="bg-blue-500 text-white rounded px-2 py-1 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50" onClick={() => redirectToTimetable(props.Name, 'f')}>View</button> : null
                } />
                <ColumnDirective field='Winter' headerText='Winter Term' width='150' textAlign='Center' template={(props) =>
                  props.Winter ? <button className="bg-blue-500 text-white rounded px-2 py-1 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50" onClick={() => redirectToTimetable(props.Name, 'w')}>View</button> : null
                } />
                <ColumnDirective field='Summer' headerText='Summer Term' width='150' textAlign='Center' template={(props) =>
                  props.Summer ? <button className="bg-blue-500 text-white rounded px-2 py-1 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50" onClick={() => redirectToTimetable(props.Name, 's')}>View</button> : null
                } />
              </ColumnsDirective>
              <Inject services={[Page]} />
            </GridComponent>
          </div>
        ) : (
          <p>No students data available.</p>
        )}
        <div className="w-80 border border-gray-300 rounded-lg px-3 py-2 mb-4 mx-auto mt-8">
          <DropDownListComponent id="ddlelement" dataSource={testData} fields={fields} placeholder="Select a test case" change={handleTestCaseChange}/>
        </div>
        <button onClick={handleGenerateDataClick} className="bg-blue-500 text-white rounded-full px-6 py-2 mt-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50">
          Generate New Data
        </button>
      </div>
    </div>
  );
};


export default IndexPage;
