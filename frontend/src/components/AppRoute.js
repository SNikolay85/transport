import React from 'react'
import Header from './Header'
import ListDrivers from './ListDrivers'
import Calendar from './Calendar'
import axios from 'axios'
import baseurl from './RoutesLinks'

class AppRoute extends React.Component
    {
        constructor(props)
            {
              super(props)

               axios.get(baseurl+'/people/driver/').then((res) => {
                      this.setState({drivers: res.data.drivers })
               })
               this.state = {
                             drivers: [],
                             }
            }
       render() {
          return(
             <div>
                <Header my_text='Дата поездки' />
                <div className="main_form">
                    <Calendar />
                </div>
                <aside>
                        <>hello</>
                </aside>
             </div>)
       }
    }

export default AppRoute
