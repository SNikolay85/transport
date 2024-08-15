import React from "react"
//import User from "./User"

class Drivers extends React.Component {
    render() {
        if (this.props.drivers.length > 0)
            return (
                <div>
                    {this.props.drivers.map((driver) => (
                        <div className="block_driver" key={driver.id_people}>
                            <h3>{driver.first_name} {driver.last_name}</h3>
                            <p>{driver.driving_licence}</p>
                        </div>
                    ))}
                </div>
            )
        else
            return (
                <div className="block_user">
                    <h3>Нет водителей</h3>
                </div>
            )
    }
}

export default Drivers