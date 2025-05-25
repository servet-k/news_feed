import React from 'react'
import bbc from "../json/bbc.json"
import cezire from "../json/cezire.json"
import sun from "../json/sun.json"
import Card from './Card'
import aa from "../json/haber.json"
import daily from "../json/daily.json"
import mirror from "../json/mirror.json"
import express from "../json/express.json"
import science from "../json/science.json"
import ensonhaber from "../json/ensonhaber.json"
import Telegraph from "../json/telegraph.json"
import NYT from "../json/New_York_Times.json"
import { useState ,useEffect} from 'react'
import './News.css';


function News() {
    const [newsData, setNewsData] = useState(aa);
    const [newsSource, setNewsSource] = useState("AA-News");
    const newsSources = {
        "AA-News": aa,
        "Ensonhaber": ensonhaber,
        "New York Times": NYT,
        "BBC": bbc,
        "Al Cezire": cezire,
        "Sun": sun,
        "Daily": daily,
        "Mirror": mirror,
        "Telegraph": Telegraph,
        "Express": express,
        "Science": science
    };
    const handleNewsChange = (newSource) => {
        setNewsSource(newSource);
        setNewsData(newsSources[newSource]);
        document.title = `${newSource} News`;
    };
    const [showBackToTop, setShowBackToTop] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            if (window.scrollY > 200) {
                setShowBackToTop(true);
            } else {
                setShowBackToTop(false);
            }
        };
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
        };
    }, []);

    const handleBackToTop = () => {
        window.scrollTo({ top: 0, behavior: 'instant' });
    };

    return (
        <div className="news-container">
            <button className="news-title">
                <span className="title-text">Latest News</span>
            </button>
            <div className="news-button-container">
                {Object.keys(newsSources).map(source => (
                    <button key={source} className="news-button" onClick={() => handleNewsChange(source)}>{source}</button>
                ))}
            </div>
            <h1 className="news-source-title">{newsSource}</h1>
            <Card data={newsData} className="news-card" />
            {showBackToTop && (
                <button
                    className="back-to-top"
                    onClick={handleBackToTop}
                >
                    Back to Top
                </button>
            )}
        </div>

    )
}

export default News