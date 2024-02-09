import React, { useState , useRef} from 'react';
import axios from 'axios';
import { Container, Form, Button, Table } from 'react-bootstrap';
import './App.css';
function App() {
  const [pnrNumber, setPnrNumber] = useState('');
  const [pnrStatus, setPnrStatus] = useState(null);
  const [error, setError] = useState('');

  const handleGetPnrStatus = async () => {
    try {
      const response = await axios.get(`https://decaptcha-pnr-backend.onrender.com/finpredict?pnrnumber=${pnrNumber}`);
      setPnrStatus(response.data);
      setError('');
      console.log(pnrStatus)
    } catch (error) {
      setPnrStatus(null);
      setError('Failed to fetch PNR status. Please check the PNR number.');
    }
  };
  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault(); // Prevent form submission
      getPnrStatusButtonRef.current.click(); // Trigger button click event
    }
  };
  const getPnrStatusButtonRef = useRef(null);
  return (
      <Container className="mt-5">
        <h1>Indian Railways PNR Status</h1>
        <Form className="my-3">
          <Form.Group controlId="pnrNumber">
            <Form.Label>Enter PNR Number:</Form.Label>
            <Form.Control
                type="text"
                value={pnrNumber}
                onChange={(e) => setPnrNumber(e.target.value)}
                onKeyDown={handleKeyPress}
            />
          </Form.Group>
          <Button ref={getPnrStatusButtonRef}
                  variant="primary"
                  onClick={handleGetPnrStatus}>
            Get PNR Status
          </Button>
        </Form>

        {pnrStatus && pnrStatus.errorMessage && <p className="text-danger">{"FLUSHED PNR/PNR not generated yet"}</p>}
        {pnrStatus && pnrStatus.arrivalDate && (

            <Table striped bordered hover className="mt-3">
              <thead>
              <tr>
                <th>Serial No</th>
                <th>Booking Berth Code</th>
                <th>Booking Berth No</th>
                <th>Booking Coach Id</th>
                <th>Booking Status</th>
              </tr>
              </thead>
              <tbody>
              {pnrStatus.passengerList.map((passenger, index) => (
                  <tr key={index}>
                    <td>{index + 1}</td>
                    <td>{passenger.bookingBerthCode}</td>
                    <td>{passenger.bookingBerthNo}</td>
                    <td>{passenger.bookingCoachId}</td>
                    <td>{passenger.bookingStatus}</td>
                  </tr>
              ))}
              </tbody>
            </Table>
        )}
      </Container>
  );
}
export default App;
