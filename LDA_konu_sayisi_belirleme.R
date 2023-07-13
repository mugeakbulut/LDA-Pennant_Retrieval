library(tidyverse)
library(ldatuning)
library(readxl)
library(topicmodels)
library(tidytext)

df <- read_xlsx("OK (1).xlsx") %>% 
  janitor::clean_names() %>% 
  select(document = docno, text = abstract) %>% 
  mutate(text = str_squish(text)) %>% 
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(document, word, sort = TRUE)

dtm_file <- df %>% 
  cast_dtm(document, word, n)

results_1 <- FindTopicsNumber(
  dtm_file,
  topics = seq(from = 10, to = 200, by = 10),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed = 77),
  mc.cores = 8L,
  verbose = TRUE
)
FindTopicsNumber_plot(results_1)
