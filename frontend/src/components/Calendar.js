import React from "react"
import DatePicker from "react-datepicker"

import "react-datepicker/dist/react-datepicker.css"

//const Calendar = () => {
//  const [startDate, setStartDate] = useState(new Date());
//  return (
//    <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
//  )
//}

class Calendar extends React.Component {
    constructor (props) {
        super(props)
        this.state = {
          startDate: new Date()
        }
        this.handleChange = this.handleChange.bind(this);
        this.onFormSubmit = this.onFormSubmit.bind(this);
      }

  handleChange(date) {
    this.setState({
      startDate: date
    })
  }

  onFormSubmit(e) {
    e.preventDefault();
    console.log(this.state.startDate)
  }

  render() {
    return (
      <form onSubmit={ this.onFormSubmit }>
        <div className="form-group">
          <DatePicker
              selected={ this.state.startDate }
              onChange={ this.handleChange }
              dateFormat="d MMMM, yyyy"
          />
          <button className="btn btn-primary">Show Date</button>
        </div>
      </form>
    );
  }


}


export default Calendar