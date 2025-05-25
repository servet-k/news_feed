import React from 'react'
import haber_resim from "./assets/haber.png"

function Card({ data }) {
  return (
    <div className="center">
      {data.map((item, index) => (
        <div className="card" key={index}>
          <img src={item.img || haber_resim} alt="haber resmi" />
          <h6>{item.time}</h6>
          <div className="property-description">
            <h5>{item.title}</h5>
            <p>{item.content.replace(/&#039;/g, "'").replace(/&quot;/g, '"')}</p>
          </div>
          <a href={item.link} target="blank">
            More...
          </a>
        </div>
      ))}
    </div>
  );
}


export default Card
