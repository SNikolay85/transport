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

               this.state = {drivers: []}
            }
       render() {
          return(
             <div>
                <Header my_text={'Дата поездки:'} content=<Calendar /> />
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
                   <ListDrivers drivers={this.state.drivers} />
                </aside>
             </div>)
       }
    }

export default AppRoute