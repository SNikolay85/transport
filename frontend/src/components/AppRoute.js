import React from 'react'
import Header from './Header'
import Drivers from './Drivers'
import ListDrivers from './ListDrivers'
import Calendar from './Calendar'
import axios from 'axios'

const baseurl = 'http://127.0.0.1:8000'

class AppRoute extends React.Component

    {
        constructor(props)
            {
              super(props)

               axios.get(baseurl+'/people/driver/').then((res) => {
                      this.setState({drivers: res.data.drivers })
               })

               axios.get(baseurl+'/driver/2024-02-01/').then((res) => {
                      this.setState({driver_date: res.data.car_carrier })
               })

               axios.get(baseurl+'/driver/2024-02-01/').then((res) => {
                     console.log(res.data.car_carrier)})

               axios.get(baseurl+'/people/driver/').then((res) => {
                     console.log(res.data.drivers)})

               this.state = {
                             drivers: [],
                             date_now: new Date(),
                             driver_date: []
                             }
            }
       render() {
          return(
             <div>
                <Header my_text='Дата поездки' />
                <Calendar />
                <div className='first_form'>
                    <select>
                        <option value={'hello'}></option>

                    </select>
                    <button>add</button>
                </div>
                <div className="main_form">
                    <Calendar />
                    <Drivers drivers={this.state.drivers} />
                </div>
                <aside>
                    <ListDrivers driver_date={this.state.driver_date} />
                </aside>
             </div>)
       }
    }

export default AppRoute