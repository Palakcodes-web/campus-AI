import { useState } from "react";
import "./App.css";

function App() {
  const [branch, setBranch] = useState("ECE AI");
  const [section, setSection] = useState("A");

  const [showLogin, setShowLogin] = useState(false);

  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const [question, setQuestion] = useState("");
  const [aiAnswer, setAiAnswer] = useState("");

  const [searchQuery, setSearchQuery] = useState("");
  const [searchResult, setSearchResult] = useState("");

  const [selectedAnnouncement, setSelectedAnnouncement] = useState("");

  const [selectedOpportunity, setSelectedOpportunity] = useState("");

  const askCampusAI = () => {
  const q = question.toLowerCase().trim();

  if (!q) {
    setAiAnswer("Type a question first and I'll help you!");
    return;
  }

  if (q.includes("python") || q.includes("assignment")) {
    setAiAnswer(
      "Your Python Lab Assignment is due tomorrow. Make sure your programs and required output are ready before submission."
    );
  } 
  else if (q.includes("electronics") || q.includes("lab")) {
    setAiAnswer(
      "Your Electronics Workshop is scheduled in Lab 3 according to the current timetable."
    );
  } 
  else if (q.includes("timetable") || q.includes("schedule")) {
    setAiAnswer(
      `You're currently viewing the ${branch} — 1st Year — Section ${section} timetable.`
    );
  } 
  else if (q.includes("hackathon")) {
    setAiAnswer(
      "The Hackathon Team Registration closes tonight at 11:59 PM. Don't miss the deadline!"
    );
  } 
  else if (q.includes("club") || q.includes("society")) {
    setAiAnswer(
      "Tech Club applications are currently open and seats are limited."
    );
  } 
  else {
    setAiAnswer(
      "I don't have enough information about that yet. Try asking about your timetable, Python assignment, labs, hackathons, or clubs."
    );
  }
};

const searchCampus = () => {
  const query = searchQuery.toLowerCase().trim();

  if (!query) {
    setSearchResult("Type something to search.");
    return;
  }

  if (query.includes("library")) {
    setSearchResult(
      "📚 Library — Find books, study spaces, and current library timings here."
    );
  } 
  else if (
    query.includes("lab 3") ||
    query.includes("electronics") ||
    query.includes("workshop")
  ) {
    setSearchResult(
      "🔬 Lab 3 — Electronics Workshop is scheduled here according to the current timetable."
    );
  } 
  else if (
    query.includes("hackathon") ||
    query.includes("competition")
  ) {
    setSearchResult(
      "🏆 Hackathon — Team registration is currently open. Check the latest deadline and announcements."
    );
  } 
  else if (
    query.includes("club") ||
    query.includes("society")
  ) {
    setSearchResult(
      "🎯 Clubs & Societies — Explore technical, cultural, speaking, sports, and other student communities."
    );
  } 
  else if (
    query.includes("cse") ||
    query.includes("ece") ||
    query.includes("it") ||
    query.includes("branch")
  ) {
    setSearchResult(
      `🎓 ${branch} — You're currently viewing the 1st Year, Section ${section} campus information.`
    );
  } 
  else if (
    query.includes("classroom") ||
    query.includes("room")
  ) {
    setSearchResult(
      "🏫 Classrooms — Search using a room number or building name to find your classroom."
    );
  } 
  else if (
    query.includes("faculty") ||
    query.includes("teacher")
  ) {
    setSearchResult(
      "👩‍🏫 Faculty — Search by faculty name, subject, or department to find relevant information."
    );
  } 
  else {
    setSearchResult(
      "🔎 I couldn't find an exact match. Try searching for Library, Lab 3, Clubs, Hackathon, Faculty, Classroom, CSE, ECE, or IT."
    );
  }
};

const showAnnouncement = (announcement) => {
  setSelectedAnnouncement(announcement);
};

  const branches = [
    "ECE AI",
    "ECE",
    "CSE AI",
    "CSE",
    "IT",
    "Robotics & Automation",
    "Mathematics & Computing",
  ];

  const timetableData = {
    "ECE AI": {
      A: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "Applied Mathematics", "B-102"],
        ["11:30 - 12:30", "Electronics Workshop", "Lab 3"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "FES", "E-201"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
      B: [
        ["09:00 - 10:00", "Applied Mathematics", "B-102"],
        ["10:15 - 11:15", "Programming Fundamentals (PF)", "A-204"],
        ["11:30 - 12:30", "Communication Skills", "C-105"],
        ["14:00 - 15:00", "Electronics Workshop", "Lab 3"],
        ["15:15 - 16:15", "Signals & Systems (SS)", "B-201"],
        ["16:15 - 17:15", "FES", "E-201"],
      ],
    },

    ECE: {
      A: [
        ["09:00 - 10:00", "Applied Mathematics", "B-102"],
        ["10:15 - 11:15", "FES", "E-201"],
        ["11:30 - 12:30", "Programming Fundamentals (PF)", "A-204"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "Electronics Workshop", "Lab 3"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
      B: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "Communication Skills", "C-105"],
        ["11:30 - 12:30", "Applied Mathematics", "B-102"],
        ["14:00 - 15:00", "FES", "E-201"],
        ["15:15 - 16:15", "Signals & Systems (SS)", "B-201"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
    },

    "CSE AI": {
      A: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "Applied Mathematics", "B-102"],
        ["11:30 - 12:30", "FES", "E-201"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "Signals & Systems (SS)", "B-201"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
      B: [
        ["09:00 - 10:00", "FES", "E-201"],
        ["10:15 - 11:15", "Programming Fundamentals (PF)", "A-204"],
        ["11:30 - 12:30", "Applied Mathematics", "B-102"],
        ["14:00 - 15:00", "Electronics Workshop", "Lab 3"],
        ["15:15 - 16:15", "Communication Skills", "C-105"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
    },

    CSE: {
      A: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "Applied Mathematics", "B-102"],
        ["11:30 - 12:30", "Communication Skills", "C-105"],
        ["14:00 - 15:00", "FES", "E-201"],
        ["15:15 - 16:15", "Electronics Workshop", "Lab 3"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
      B: [
        ["09:00 - 10:00", "Applied Mathematics", "B-102"],
        ["10:15 - 11:15", "FES", "E-201"],
        ["11:30 - 12:30", "Programming Fundamentals (PF)", "A-204"],
        ["14:00 - 15:00", "Signals & Systems (SS)", "B-201"],
        ["15:15 - 16:15", "Communication Skills", "C-105"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
    },

    IT: {
      A: [
        ["09:00 - 10:00", "Applied Mathematics", "B-102"],
        ["10:15 - 11:15", "Programming Fundamentals (PF)", "A-204"],
        ["11:30 - 12:30", "FES", "E-201"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "Electronics Workshop", "Lab 3"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
      B: [
        ["09:00 - 10:00", "Communication Skills", "C-105"],
        ["10:15 - 11:15", "Applied Mathematics", "B-102"],
        ["11:30 - 12:30", "Programming Fundamentals (PF)", "A-204"],
        ["14:00 - 15:00", "FES", "E-201"],
        ["15:15 - 16:15", "Signals & Systems (SS)", "B-201"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
    },

    "Robotics & Automation": {
      A: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "FES", "E-201"],
        ["11:30 - 12:30", "Applied Mathematics", "B-102"],
        ["14:00 - 15:00", "Electronics Workshop", "Lab 3"],
        ["15:15 - 16:15", "Communication Skills", "C-105"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
      B: [
        ["09:00 - 10:00", "FES", "E-201"],
        ["10:15 - 11:15", "Applied Mathematics", "B-102"],
        ["11:30 - 12:30", "Programming Fundamentals (PF)", "A-204"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "Electronics Workshop", "Lab 3"],
        ["16:15 - 17:15", "Signals & Systems (SS)", "B-201"],
      ],
    },

    "Mathematics & Computing": {
      A: [
        ["09:00 - 10:00", "Applied Mathematics", "B-102"],
        ["10:15 - 11:15", "Programming Fundamentals (PF)", "A-204"],
        ["11:30 - 12:30", "Signals & Systems (SS)", "B-201"],
        ["14:00 - 15:00", "Communication Skills", "C-105"],
        ["15:15 - 16:15", "FES", "E-201"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
      B: [
        ["09:00 - 10:00", "Programming Fundamentals (PF)", "A-204"],
        ["10:15 - 11:15", "Signals & Systems (SS)", "B-201"],
        ["11:30 - 12:30", "Applied Mathematics", "B-102"],
        ["14:00 - 15:00", "FES", "E-201"],
        ["15:15 - 16:15", "Communication Skills", "C-105"],
        ["16:15 - 17:15", "Electronics Workshop", "Lab 3"],
      ],
    },
  };

const showOpportunity = (opportunity) => {
  setSelectedOpportunity(opportunity);
};


  const timetable = timetableData[branch][section];

  return (
    <div className="dashboard">

      {/* NAVBAR */}
      <nav className="navbar">
        <div className="logo">CampusAI</div>

        <div className="nav-links">
          <a href="#dashboard">Dashboard</a>
          <a href="#announcements">Announcements</a>
          <a href="#timetable">Timetable</a>
          <a href="#opportunities">Opportunities</a>
        </div>

        <button
  className="profile"
  onClick={() => {
    if (isLoggedIn) {
      setIsLoggedIn(false);
    } else {
      setShowLogin(true);
    }
  }}
>
  {isLoggedIn ? "✓ Logged in" : "Login"}
</button>
      </nav>

      {showLogin && (
  <div className="login-overlay">
    <div className="login-card">

      <button
        className="login-close"
        onClick={() => setShowLogin(false)}
      >
        ×
      </button>

      <p className="eyebrow">CAMPUSAI</p>

      <h2>Welcome back 👋</h2>

      <p>Login to access your campus dashboard.</p>

      <input
        type="text"
        placeholder="Student Email / ID"
      />

      <input
        type="password"
        placeholder="Password"
      />

      <button
  className="login-submit"
  onClick={() => {
  alert("✅ Login successful! Welcome to CampusAI.");
  setIsLoggedIn(true);
  setShowLogin(false);
}}
>
  Login →
</button>

    </div>
  </div>
)}


      {/* WELCOME */}
      <section className="welcome" id="dashboard">
        <p className="eyebrow">YOUR CAMPUS COMMAND CENTER</p>

        <h1>
          Good morning, <span>Palak.</span>
        </h1>

        <p className="subtitle">
          Here's what actually matters today.
        </p>

        <div className="status">
          <span></span> CampusAI is active
        </div>
      </section>


      {/* PRIORITIES */}
      <section className="section">
        <div className="section-heading">
          <h2>Today's Priorities</h2>
          <span>AI SORTED</span>
        </div>

        <div className="priority-grid">

          <div className="priority-card urgent">
            <div className="card-top">
              <span>URGENT</span>
              <span>→</span>
            </div>

            <h3>Hackathon Registration</h3>
            <p>Registration closes today at 11:59 PM.</p>
          </div>

          <div className="priority-card">
            <div className="card-top">
              <span>ACADEMIC</span>
              <span>→</span>
            </div>

            <h3>Python Lab Assignment</h3>
            <p>Submission deadline is tomorrow.</p>
          </div>

          <div className="priority-card">
            <div className="card-top">
              <span>OPPORTUNITY</span>
              <span>→</span>
            </div>

            <h3>Tech Club Applications</h3>
            <p>Limited seats available.</p>
          </div>

        </div>
      </section>


      {/* AI ASSISTANT */}
      <section className="ai-section">
        <div className="ai-glow"></div>

        <p className="eyebrow">CAMPUSAI</p>

        <h2>Ask anything about your campus.</h2>

        <p>
          From classrooms to clubs, deadlines to opportunities —
          get clear answers instantly.
        </p>

<div className="ai-search">

  <input
    type="text"
    placeholder="Ask CampusAI anything..."
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
    onKeyDown={(e) => {
      if (e.key === "Enter") {
        askCampusAI();
      }
    }}
  />

  <button onClick={askCampusAI}>
    Ask AI →
  </button>

</div>

{aiAnswer && (
  <div className="ai-answer">
    <div className="ai-answer-label">
      CAMPUSAI
    </div>

    <p>{aiAnswer}</p>
  </div>
)}      
      </section>


      {/* TIMETABLE */}
      <section className="section" id="timetable">

        <div className="section-heading">
          <h2>Today's Timetable</h2>
          <span>1ST YEAR</span>
        </div>

        {/* FILTERS */}
        <div className="timetable-filters">

          <select
            value={branch}
            onChange={(e) => setBranch(e.target.value)}
          >
            {branches.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>

          <select
            value={section}
            onChange={(e) => setSection(e.target.value)}
          >
            <option value="A">Section A</option>
            <option value="B">Section B</option>
          </select>

        </div>


        {/* CURRENT SELECTION */}
        <div className="selected-timetable">
          <p>
            Showing timetable for{" "}
            <strong>{branch}</strong> —{" "}
            <strong>1st Year</strong> —{" "}
            <strong>Section {section}</strong>
          </p>
        </div>


        {/* TIMETABLE */}
        <div className="timetable-list">

          {timetable.map((item, index) => (
            <div
              className={`timetable-card ${
                index === 0 ? "now" : ""
              }`}
              key={index}
            >

              <div className="time">
                {item[0]}
              </div>

              <div className="subject">
                <h3>{item[1]}</h3>
                <p>Room {item[2]}</p>
              </div>

              {index === 0 && (
                <div className="now-badge">
                  NOW
                </div>
              )}

            </div>
          ))}

        </div>

      </section>


      {/* LOWER GRID */}
      <section className="content-grid">

        <div className="content-card">
          <div className="card-title">
            <h2>Upcoming Deadlines</h2>
          </div>

          <div className="deadline">
            <span>15 SEP</span>
            <p>Python Assignment</p>
          </div>

          <div className="deadline">
            <span>18 SEP</span>
            <p>Club Registration</p>
          </div>

          <div className="deadline">
            <span>21 SEP</span>
            <p>Mid-Sem Registration</p>
          </div>
        </div>


        <div className="content-card" id="announcements"></div>
          <div className="card-title">
            <h2>Important Announcements</h2>
          </div>

<button
  className="announcement-item"
  onClick={() =>
    showAnnouncement(
      "📢 Freshers Orientation — Venue has been changed. Please check the updated venue before attending."
    )
  }
>
  📢 Freshers Orientation — Venue changed →
</button>

<button
  className="announcement-item"
  onClick={() =>
    showAnnouncement(
      "📚 Library timing has been updated. Check the latest timing before planning your study session."
    )
  }
>
  📚 Library timing has been updated →
</button>

<button
  className="announcement-item"
  onClick={() =>
    showAnnouncement(
      "🏆 Hackathon Team Registration closes tonight. Make sure your team registration is completed before the deadline."
    )
  }
>
  🏆 Hackathon Team Registration closes tonight →
</button>

{selectedAnnouncement && (
  <div className="announcement-detail">
    <p>{selectedAnnouncement}</p>

    <button onClick={() => setSelectedAnnouncement("")}>
      Close
    </button>
    {selectedAnnouncement && (
  <div className="announcement-detail">
    <p>{selectedAnnouncement}</p>

    <button onClick={() => setSelectedAnnouncement("")}>
      Close
    </button>
  </div>
)}
  </div>
)}


        <div className="content-card" id="opportunities">
          <div className="card-title">
            <h2>Recommended Opportunities</h2>
          </div>

          <div className="opportunity-item">
  <h3>🤖 AI/ML Workshop</h3>
  <p>Learn the basics of AI and Machine Learning through a practical workshop.</p>
  <span>📅 Deadline: 20 Sep</span>
  <button
  onClick={() =>
    showOpportunity(
      "🤖 AI/ML Workshop — Hands-on session with practical activities, beginner-friendly guidance, and an opportunity to build your first small AI/ML concept. No prior experience required."
    )
  }
>
  View Opportunity →
</button>
</div>

<div className="opportunity-item">
  <h3>💡 Campus Hackathon</h3>
  <p>Build a creative solution with your team and compete with other students.</p>
  <span>⏳ Limited Seats</span>
  <button
  onClick={() =>
    showOpportunity(
      "💡 Campus Hackathon — Form a team, choose a problem, build a prototype, and present your solution to the judges. A great chance to collaborate, experiment, and showcase your skills."
    )
  }
>
  View Opportunity →
</button>
</div>

<div className="opportunity-item">
  <h3>🚀 Tech Society</h3>
  <p>Join the technical community and explore workshops, projects and events.</p>
  <span>🎓 Open for 1st Year</span>
  <button
  onClick={() =>
    showOpportunity(
      "🚀 Tech Society — Join a community of students interested in technology. Take part in coding sessions, technical projects, hackathons, peer learning, and society events."
    )
  }
>
  View Opportunity →
</button>
</div>{selectedOpportunity && (
  <div className="opportunity-detail">
    <p>{selectedOpportunity}</p>

    <button onClick={() => setSelectedOpportunity("")}>
      Close
    </button>
  </div>
)}
        </div>

      </section>


      {/* CAMPUS SEARCH */}
      <section className="campus-search">

        <p className="eyebrow">EXPLORE YOUR CAMPUS</p>

       <h2>Search Campus Information</h2>

       <div className="search-box">
        <input
      type="text"
      placeholder="Search rooms, clubs, faculty, events..."
      value={searchQuery}
      onChange={(e) => setSearchQuery(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") {
          searchCampus();
        }
      }}
    />

    <button onClick={searchCampus}>
      Search →
    </button>
  </div>

  {searchResult && (
    <div className="search-result">
      <p>{searchResult}</p>
    </div>
  )}

</section>


      {/* FOOTER */}
      <footer>
        <strong>CampusAI</strong>
        <p>Turning campus chaos into clarity.</p>
      </footer>

    </div>
  );
}

export default App;