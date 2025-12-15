from llm_playground.brochure import BrochureGenerator


def main(company_name: str, url: str):
    brochure_generator = BrochureGenerator(url)
    brochure = brochure_generator.create_brochure(company_name)
    return brochure
if __name__ == "__main__":
    # test_url = "https://huggingface.co"
    test_url = "https://boskalis.com/"
    test_company_name = "Hugging Face"
    test_company_name = "Boskalis"
    result = main(company_name=test_company_name, url=test_url)

