from selenium import webdriver
from bs4 import BeautifulSoup

class BrowserService():
    def __init__(self):
        self.driver=webdriver.Chrome()
       
    def open_url(self,app_url):
        print(app_url)
        self.driver.get(app_url)

    def get_dom(self):
        return self.driver.page_source

    def take_screenshots(self,path):
        self.driver.save_screenshot(path)

    def get_page_text(self):
        return self.driver.find_element("tag name","body").text

    def close(self):
        self.driver.quit()

    


    def get_compact_dom(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        elements = []

        semantic_tags = {
            "form",
            "fieldset",
            "section",
            "article",
            "main",
            "nav"
        }

        for element in soup.find_all([
            "input",
            "button",
            "select",
            "textarea",
            "a",
            "option"
        ]):

            attributes = []

            # Generic HTML attributes useful for QA
            for attr in [
                "type",
                "id",
                "name",
                "value",
                "placeholder",
                "aria-label",
                "role",
                "title",
                "onclick",
                "onchange",
                "onsubmit",
                "oninput"
            ]:
                value = element.get(attr)

                if value:
                    attributes.append(f"{attr}={value}")

            # Associated label
            element_id = element.get("id")

            if element_id:
                label = soup.find(
                    "label",
                    attrs={"for": element_id}
                )

                if label:
                    label_text = label.get_text(" ", strip=True)

                    if label_text:
                        attributes.append(f"label={label_text}")

            # Visible text
            text = element.get_text(" ", strip=True)

            if text:
                attributes.append(f"text={text}")

            # Element states
            for state in [
                "checked",
                "disabled",
                "required",
                "selected"
            ]:
                if element.has_attr(state):
                    attributes.append(
                        f"{state}=true"
                    )

            # Current semantic parent/context
            parent_context = self.get_parent_context(element, semantic_tags)

            if parent_context:
                attributes.append(f"parent={parent_context}")

            elements.append(f"{element.name}: " + ", ".join(attributes))

        return "\n".join(elements)
    

    def get_parent_context(self,element,semantic_tags):
        parent = element.parent
            
        while parent:
            if parent.name in semantic_tags:
            # Prefer meaningful identifying attributes
                context = []
                for attr in ["id", "name", "role", "aria-label", "title"]:
                    value = parent.get(attr)
                    if value:
                        context.append(f"{attr}={value}")

                # Add parent text only when there is no useful identifier
                if not context:
                    text = parent.get_text(" ", strip=True)

                    if text:
                        text = " ".join(text.split())

                        if len(text) > 150:
                            text = text[:150] + "..."

                        context.append(f"text={text}")

                if context:
                    return " | ".join(context)
            parent = parent.parent
            
        return "" 