from pathlib import Path
import base64
import json
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Sami Kazemi Resume", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "img"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def load_resume() -> dict:
    data_file = DATA_DIR / "resume.json"
    if data_file.exists():
        return json.loads(read_text(data_file))
    else:
        st.error(f"❌ Missing required file: {data_file}")
        st.stop()  # Halt execution gracefully
    return {}



def build_avatar_tag(use_video=False) -> str:
    video_path = IMG_DIR / "video.mp4"
    img_path = IMG_DIR / "pic1.jpg"

    if use_video and video_path.exists():
        b64 = base64.b64encode(video_path.read_bytes()).decode("utf-8")
        return f"""
        <video autoplay muted loop playsinline
               style='width:100%;height:100%;object-fit:cover;display:block;border-radius:0;'>
            <source src='data:video/mp4;base64,{b64}' type='video/mp4' />
        </video>"""
    
    if img_path.exists():
        b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
        return f"<img src='data:image/jpeg;base64,{b64}' alt='Profile' style='width:100%;height:100%;object-fit:cover;display:block;border-radius:0;' />"
    
    return "<div style='width:170px;height:170px;background:#3b82f6;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:32px;color:white;'>SK</div>"


def progress_skill_li(name: str, percent: int) -> str:
    percent_text = f"{percent}%"
    return (
        "<div class='skill-item'>"
        f"<div class='skill-label'><span>{name}</span><span>{percent_text}</span></div>"
        f"<div class='skill-bar-container'><div class='skill-bar-fill' style='width: {percent}%;'></div></div>"
        "</div>"
    )


def dict_to_progress_list(d: dict) -> str:
    html = ""
    for name, value in d.items():
        try:
            percent = int(float(value))
        except (ValueError, TypeError):
            percent = 85
        html += progress_skill_li(name, percent)
    return html


def interpersonal_skills_to_html(skills) -> str:
    html = "<div class='interpersonal-grid'>"
    items = []
    
    if isinstance(skills, list):
        for s in skills:
            if isinstance(s, dict):
                items.append(s)
            else:
                items.append({"name": str(s)})
    
    for skill in items[:4]:
        name = skill.get("name", "Skill")
        image_file = skill.get("image", f"{name.lower().replace(' ', '-')}.png")
        img_path = IMG_DIR / image_file

        if img_path.exists():
            b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
            img_tag = f"<img src='data:image/png;base64,{b64}' alt='{name}' />"
        else:
            img_tag = (
                "<div style='background:#e0e7ef;color:#6b7280;font-size:24px;"
                "width:100%;height:100%;display:flex;align-items:center;"
                "justify-content:center;'>?</div>"
            )

        html += (
            f"<div class='skill-circle-item'>"
            f"<div class='skill-circle'>{img_tag}</div>"
            f"<p class='skill-circle-name'>{name}</p>"
            "</div>"
        )
    
    html += "</div>"
    return html


def languages_to_progress_bars(languages: list) -> str:
    level_map = {
        "Proficient": 90, "Fluent": 95, "Intermediate": 60,
        "Mother tongue": 100, "Native": 100, "Basic": 40
    }
    
    html = ""
    for lang in languages[:3]:
        name = lang.get("name", "Language")
        level_text = lang.get("level", "Unknown")
        percent = level_map.get(level_text, 60)

        html += f"""
        <div class="language-box">
          <div class="language-name-part">{name}</div>
          <div class="language-progress-part">
            <div class="language-progress-fill" style="width: {percent}%;"></div>
            <div class="language-progress-percent">{percent}%</div>
          </div>
        </div>
        """
    return html


def experience_to_html(experience: list) -> str:
    """Render experience using YOUR JSON structure: role, company, period, bullets."""
    if not experience:
        return "<p style='text-align:center;color:#6b7280;'>No experience listed</p>"
    
    html = ""
    for exp in experience:
        if not exp.get("enabled", True):
            continue
            
        # Logo (your field: "logo")
        logo_html = ""
        logo_file = exp.get("logo")
        if logo_file:
            img_path = IMG_DIR / logo_file
            if img_path.exists():
                b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                logo_html = f"""
                <div class="exp-logo">
                  <img src="data:image/png;base64,{b64}" alt="{exp.get('company', '')}" />
                </div>
                """
        
        # YOUR fields: company, role, period
        company = exp.get("company", "")
        role = exp.get("role", "")
        period = exp.get("period", "")
        
        # Bullets (your field: "bullets")
        bullets = exp.get("bullets", [])
        bullets_html = ""
        if bullets:
            bullets_html = "<ul class='exp-bullets'>"
            for bullet in bullets:
                bullets_html += f"<li>{bullet}</li>"
            bullets_html += "</ul>"
        
        html += f"""
        <div class="exp-entry">
        {logo_html}
        <div class="exp-header">
            <div class="exp-company">{company} <span class="exp-year">({period})</span></div>
            <div class="exp-role">{role}</div>
        </div>
        <div class="exp-description">{bullets_html}</div>
        </div>
        """

    
    return html

def education_to_html(education: list) -> str:
    """Render education with logos + clickable thesis links."""
    if not education:
        return "<p style='text-align:center;color:#6b7280;'>No education listed</p>"
    
    html = ""
    for edu in education:
        if not edu.get("enabled", True):
            continue
            
        # Logo
        logo_html = ""
        logo_file = edu.get("logo")
        if logo_file:
            img_path = IMG_DIR / logo_file
            if img_path.exists():
                b64 = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                logo_html = f"""
                <div class="edu-logo">
                  <img src="data:image/png;base64,{b64}" alt="{edu.get('institution', '')}" />
                </div>
                """
        
        # Main fields
        degree = edu.get("degree", "")
        institution = edu.get("institution", "")
        period = edu.get("period", "")
        field = edu.get("field", "")
        notes = edu.get("notes", "")
       
        
        # Bullets including thesis as bullet
        bullets = edu.get("bullets", [])
        thesis_title = edu.get("thesis_title", "")
        thesis_link = edu.get("thesis_link", "")

        bullets_html = ""
        if bullets or (thesis_title and thesis_link):
            bullets_html = "<ul class='edu-bullets'>"
            
            # Regular bullets
            for bullet in bullets:
                bullets_html += f"<li>{bullet}</li>"
            
            # Thesis as bullet
            if thesis_title and thesis_link:
                bullets_html += f"""
                <li>
                    Thesis: <a class="thesis-link" href="{thesis_link}" target="_blank">{thesis_title}</a>
                </li>
                """
            
            bullets_html += "</ul>"

        # Insert into main HTML
        html += f"""
        <div class="edu-entry">
        {logo_html}
        <div class="edu-header">
            <div class="edu-degree">{degree}</div>
            <div class="edu-institution">{institution} <span class="edu-year">({period})</span></div>
        </div>
        <div class="edu-details">
            <div class="edu-field">{field} <span class="edu-notes">({notes})</span></div>
            <div class="edu-description">{bullets_html}</div>
            
        </div>
        </div>
        """
    return html

def courses_to_html(courses: list) -> str:
    if not courses:
        return "<p style='text-align:center;color:#6b7280;'>No courses listed</p>"

    # Prepare badge background once
    badge_b64 = ""
    badge_path = IMG_DIR / "badge.png"
    if badge_path.exists():
        badge_b64 = base64.b64encode(badge_path.read_bytes()).decode("utf-8")

    html = "<div class='courses-row'>"
    for course in courses:
        if not course.get("enabled", True):
            continue

        field = course.get("name", "")
        year = course.get("period", "")
        logo_file = course.get("logo")

        logo_html = ""
        if logo_file:
            logo_path = IMG_DIR / logo_file
            if logo_path.exists():
                logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
                logo_html = (
                    f"<img class='course-logo-inside' "
                    f"src='data:image/png;base64,{logo_b64}' alt='{field}'>"
                )

        badge_style = (
            f"style=\"background-image:url('data:image/png;base64,{badge_b64}');\""
            if badge_b64 else ""
        )

        html += f"""
        <div class="course-item">
          <div class="course-badge" {badge_style}>
            {logo_html}
          </div>
          <div class="course-name">{field}</div>
          <div class="course-year">{year}</div>
        </div>
        """

    html += "</div>"
    return html

def projects_to_html(projects: list) -> str:
    if not projects:
        return "<p style='text-align:center;color:#6b7280;'>No courses listed</p>"

    

    html = "<div class='courses-row'>"
    for project in projects:
        if not project.get("enabled", True):
            continue

        field = project.get("name", "")
        year = project.get("period", "")
        logo_file = project.get("logo")
        link = project.get("link", "#")
        logo_html = ""
        if logo_file:
            logo_path = IMG_DIR / logo_file
            if logo_path.exists():
                logo_b64 = base64.b64encode(logo_path.read_bytes()).decode("utf-8")
                logo_html = (
                    f"<img class='project-logo-inside' "
                    f"src='data:image/png;base64,{logo_b64}' alt='{field}'>"
                )

        
        html += f"""
        <div class="course-item">
          <div class="project-square">
            {logo_html}
          </div>
        <a href='{link}' class="project-name" target="_blank">{field}</a>          <div class="project-year">{year}</div>
        </div>
        """

    html += "</div>"
    return html



def main():
    html_template = read_text(STATIC_DIR / "index.html")
    css = read_text(STATIC_DIR / "style.css")

    data = load_resume()
    contact = data.get("contact", {})
    references = data.get("references", [])

    # Avatar
    avatar_tag = build_avatar_tag(use_video=False)

    # References with links
    refs_html = ""
    if references:
        refs_html = (
            "<ul class='reference-list'>"
            + "".join(
                f"<li><a class='reference-link' href='mailto:{r.get('email', '')}'>{r.get('name', '')} ({r.get('title', '')})</a></li>"
                for r in references if r.get("enabled", True)
            )
            + "</ul>"
        )
    else:
        refs_html = "<p class='reference-none' style='text-align:center;color:#6b7280;'>Available upon request</p>"

    # Right column
    technical_skills = data.get("technical_skills", {})
    interpersonal_skills = data.get("interpersonal_skills", [])
    languages = data.get("languages", [])

    technical_html = dict_to_progress_list(technical_skills)
    interpersonal_html = interpersonal_skills_to_html(interpersonal_skills)
    languages_html = languages_to_progress_bars(languages)

    # Middle column
    pitch = data.get("pitch", "")
    experience_html = experience_to_html(data.get("experience", []))  # "experiences" plural
    education_html = education_to_html(data.get("education", []))
    projects_html = projects_to_html(data.get("projects", []))
    courses_html = courses_to_html(data.get("courses", []))

    # Replace all placeholders
    html_content = html_template
    html_content = html_content.replace("{{INLINE_CSS}}", f"<style>{css}</style>")
    html_content = html_content.replace("{{IMG_TAG}}", avatar_tag)
    html_content = html_content.replace("{{NAME}}", data.get("name", ""))
    html_content = html_content.replace("{{TITLE}}", data.get("title", ""))
    raw_phone = contact.get("phone", "")          # "+358 44 519 5357"
    phone_e164 = "".join(ch for ch in raw_phone if ch.isdigit())  # "358445195357"

    html_content = html_content.replace("{{EMAIL}}", contact.get("email", ""))
    html_content = html_content.replace("{{PHONE}}", raw_phone)
    html_content = html_content.replace("{{PHONE_E164}}", phone_e164)
    html_content = html_content.replace("{{LOCATION}}", contact.get("location", ""))
    html_content = html_content.replace("{{WEBSITE}}", contact.get("website", ""))
    html_content = html_content.replace("{{LINKEDIN}}", contact.get("linkedin", "#"))
    html_content = html_content.replace("{{GITHUB}}", contact.get("github", "#"))
    html_content = html_content.replace("{{REFERENCES}}", refs_html)
    
    # Middle sections
    html_content = html_content.replace("{{PITCH}}", pitch)
    html_content = html_content.replace("{{EXPERIENCE}}", experience_html)
    html_content = html_content.replace("{{EDUCATION}}", education_html)
    html_content = html_content.replace("{{COURSES}}", courses_html)
    html_content = html_content.replace("{{PROJECTS}}", projects_html)
    
    # Right column
    html_content = html_content.replace("{{TECHNICAL_SKILLS}}", technical_html)
    html_content = html_content.replace("{{INTERPERSONAL_SKILLS}}", interpersonal_html)
    html_content = html_content.replace("{{LANGUAGES_RIGHT}}", languages_html)

    # Streamlit styling
    st.markdown("""
    <style>
    .block-container { padding: 0 !important; margin: 0 !important;
                       height: 100vh !important; overflow: hidden !important; }
    .stApp { height: 100vh !important; overflow: hidden !important;
             background-color: #020617 !important; padding: 0 !important; }
    iframe { height: 860px !important; width: 100% !important;
             border: none !important; overflow: hidden !important; }
    header[data-testid="stHeader"], footer { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    components.html(html_content, height=860, scrolling=False)


if __name__ == "__main__":
    main()
