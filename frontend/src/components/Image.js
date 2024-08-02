import React from "react"

class Image extends React.Component {
    render() {
           return (
           <img className='logo_pic' src={this.props.my_image} alt="description"/>
           )
    }
}

export default Image