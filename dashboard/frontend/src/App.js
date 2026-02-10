import { useState, useEffect } from 'react';
import axios from 'axios';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
    ResponsiveContainer, ReferenceLine
} from 'recharts';
import './App.css';

const API_BASE_URL = 'http://localhost:5000/api';

function App() {
    const [priceData, setPriceData] = useState([]);
    const [events, setEvents] = useState([]);
    const [changepoints, setChangepoints] = useState([]);
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [dateRange, setDateRange] = useState({ start: '2015-01-01', end: '2023-12-31' });
    const [selectedCategory, setSelectedCategory] = useState('All');

    useEffect(() => {
        fetchData();
    }, [dateRange, selectedCategory]);

    const fetchData = async () => {
        setLoading(true);
        try {
            // Fetch prices
            const pricesRes = await axios.get(`${API_BASE_URL}/prices/range`, {
                params: { start_date: dateRange.start, end_date: dateRange.end }
            });
            setPriceData(pricesRes.data.data);

            // Fetch events
            const eventsParams = selectedCategory !== 'All' ? { category: selectedCategory } : {};
            const eventsRes = await axios.get(`${API_BASE_URL}/events`, { params: eventsParams });
            setEvents(eventsRes.data.data);

            // Fetch change points
            const cpRes = await axios.get(`${API_BASE_URL}/changepoints`);
            setChangepoints(cpRes.data.data);

            // Fetch summary
            const summaryRes = await axios.get(`${API_BASE_URL}/summary`);
            setSummary(summaryRes.data.data);

            setLoading(false);
        } catch (error) {
            console.error('Error fetching data:', error);
            setLoading(false);
        }
    };

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            return (
                <div className="custom-tooltip">
                    <p><strong>Date:</strong> {payload[0].payload.Date}</p>
                    <p><strong>Price:</strong> ${payload[0].value.toFixed(2)}/barrel</p>
                </div>
            );
        }
        return null;
    };

    if (loading) {
        return <div className="loading">Loading dashboard...</div>;
    }

    return (
        <div className="App">
            <header className="App-header">
                <h1>🛢️ Brent Oil Price Change Point Analysis</h1>
                <p>Interactive Dashboard - Birhan Energies</p>
            </header>

            {/* Summary Cards */}
            {summary && (
                <div className="summary-cards">
                    <div className="card">
                        <h3>Total Observations</h3>
                        <p className="stat">{summary.price_statistics.count.toLocaleString()}</p>
                    </div>
                    <div className="card">
                        <h3>Average Price</h3>
                        <p className="stat">${summary.price_statistics.mean.toFixed(2)}</p>
                    </div>
                    <div className="card">
                        <h3>Price Range</h3>
                        <p className="stat">
                            ${summary.price_statistics.min.toFixed(2)} - ${summary.price_statistics.max.toFixed(2)}
                        </p>
                    </div>
                    <div className="card">
                        <h3>Events Tracked</h3>
                        <p className="stat">{summary.total_events}</p>
                    </div>
                    <div className="card">
                        <h3>Change Points</h3>
                        <p className="stat">{summary.changepoints_detected}</p>
                    </div>
                </div>
            )}

            {/* Filters */}
            <div className="filters">
                <div className="filter-group">
                    <label>Start Date:</label>
                    <input
                        type="date"
                        value={dateRange.start}
                        onChange={(e) => setDateRange({ ...dateRange, start: e.target.value })}
                    />
                </div>
                <div className="filter-group">
                    <label>End Date:</label>
                    <input
                        type="date"
                        value={dateRange.end}
                        onChange={(e) => setDateRange({ ...dateRange, end: e.target.value })}
                    />
                </div>
                <div className="filter-group">
                    <label>Event Category:</label>
                    <select
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="All">All Events</option>
                        <option value="Geopolitical">Geopolitical</option>
                        <option value="Economic">Economic</option>
                        <option value="OPEC">OPEC Policy</option>
                    </select>
                </div>
                <button onClick={fetchData} className="refresh-btn">Refresh Data</button>
            </div>

            {/* Main Price Chart */}
            <div className="chart-container">
                <h2>Historical Brent Oil Prices with Change Points</h2>
                <ResponsiveContainer width="100%" height={400}>
                    <LineChart data={priceData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis
                            dataKey="Date"
                            tick={{ fontSize: 12 }}
                            angle={-45}
                            textAnchor="end"
                            height={80}
                        />
                        <YAxis label={{ value: 'Price (USD/barrel)', angle: -90, position: 'insideLeft' }} />
                        <Tooltip content={<CustomTooltip />} />
                        <Legend />
                        <Line
                            type="monotone"
                            dataKey="Price"
                            stroke="#2E86AB"
                            dot={false}
                            strokeWidth={2}
                            name="Brent Oil Price"
                        />
                        {/* Add change point markers */}
                        {changepoints.map((cp, idx) => (
                            <ReferenceLine
                                key={idx}
                                x={cp.date}
                                stroke="red"
                                strokeDasharray="3 3"
                                label={{ value: 'Change Point', position: 'top', fill: 'red' }}
                            />
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            </div>

            {/* Events Timeline */}
            <div className="chart-container">
                <h2>Geopolitical & Economic Events</h2>
                <div className="events-list">
                    {events.map((event, idx) => (
                        <div key={idx} className={`event-item ${event.category.toLowerCase()}`}>
                            <div className="event-date">{event.date}</div>
                            <div className="event-content">
                                <h4>{event.event_name}</h4>
                                <span className="event-category">{event.category}</span>
                                <p>{event.description}</p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Change Points Summary */}
            {changepoints.length > 0 && (
                <div className="chart-container">
                    <h2>Detected Change Points</h2>
                    <div className="changepoints-list">
                        {changepoints.map((cp, idx) => (
                            <div key={idx} className="changepoint-item">
                                <h4>Change Point {idx + 1}</h4>
                                <p><strong>Date:</strong> {cp.date}</p>
                                <p><strong>Posterior Probability:</strong> {(cp.probability * 100).toFixed(2)}%</p>
                                <p><strong>95% HPD Interval:</strong> [{cp.hpd_lower}, {cp.hpd_upper}]</p>
                                <p><strong>Mean Before:</strong> {cp.mu_before.toFixed(6)}</p>
                                <p><strong>Mean After:</strong> {cp.mu_after.toFixed(6)}</p>
                                <p><strong>Volatility (σ):</strong> {cp.sigma.toFixed(4)}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            <footer className="App-footer">
                <p>© 2026 Birhan Energies | Brent Oil Price Change Point Analysis</p>
                <p>Data Science Team | Task 3: Interactive Dashboard</p>
            </footer>
        </div>
    );
}

export default App;
