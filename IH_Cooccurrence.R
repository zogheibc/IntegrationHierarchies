##load packages
library(readr)
library(tidyverse)
library(cooccur)
library(visNetwork)
library(data.table)


##import data
themedata <- read_csv("IH_ThemesQuant.csv", 
                      col_types = cols(DataAndInfo = col_number(), 
                                       KnowledgeAndPerspective = col_number(), 
                                       ProgramAndOrganization = col_number(), Technology = col_number(), 
                                       CommunitiesAndPeople = col_number(), 
                                       Crossdisciplinarity = col_number(), 
                                       Research = col_number(), Innovation = col_number(), 
                                       Other = col_number()))

##replace NAs with 0
themedata[is.na(themedata)] <- 0

##make quote IDs into row names
themedata2 <- themedata[,-1]
rownames(themedata2) <- themedata[,1]

#change column names
themedata2 <- themedata2 |>
  rename("Communities and People" = CommunitiesAndPeople,
         "Programs and Organizations" = ProgramAndOrganization,
         "Knowledge and Perspectives" = KnowledgeAndPerspective,
         "Data and Information" = DataAndInfo)

#transpose data frame
themedata3 <- transpose(themedata2)
#redefine row and column names
rownames(themedata3) <- colnames(themedata2)
colnames(themedata3) <- rownames(themedata2)

##do cooccurence analysis
co <- print(cooccur(themedata3, spp_names = TRUE))
##to interpret results: 
  ##we're using a threshold to only see significant results
  ##if the p_lt column is <0.05 then the two terms occur together LESS frequently than expected by chance
  ##if the p_gt column is <0.05 then the two terms occur together MORE frequently than expected by chance
  ##sp1_inc is number of samples that have theme 1
  ##sp2_inc is number of samples that have theme 2
  ##obs_cooccur is the observed number of samples having both themes
  ##prob_cooccur is the probability that both themes occur in a sample
  ##exp_cooccur is the expected number of samples having both themes (assuming random distribution of themes)


##NETWORK ANALYSIS

##make nodes dataframe 
##colours from https://personal.sron.nl/~pault/#sec:qualitative 
nodes <- data.frame(id = 1:nrow(themedata3),
                    label = rownames(themedata3),
                    color = c("#332288","#88CCEE","#44AA99", "#117733", "#DDCC77", "#CC6677", "#882255","#AA4499","#BBBBBB"),
                    shadow = TRUE) 
##now make edges dataframe from the significant cooccurences we calculated earlier
edges <- data.frame(from = co$sp1, to = co$sp2, #undirected network so to/from doesn't matter
                    color = ifelse(co$p_lt <= 0.05, "#B0B2C1", "#3C3F51"),
                                   dashes = ifelse(co$p_lt <= 0.05, TRUE, FALSE))
##now plot our network (different layout options commented out)
visNetwork(nodes = nodes, edges = edges) |>
  visIgraphLayout(layout = "layout_on_grid") |>
  visNodes(font = list(size = 14, color = "#000000"))
  #visIgraphLayout(layout = "layout_with_kk")
  #visIgraphLayout(layout = "layout_with_sugiyama")

# visNetwork(nodes = nodes, edges = edges) |>
#   visIgraphLayout(layout = "layout_on_grid")

