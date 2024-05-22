from guardiannews.runner import Run

runner = Run()  # membuat object

if __name__ == '__main__':
    # runner.scrape_category()
    runner.scrape_by_category_opinion()
