##load packages
library(readr)
library(tidyverse)
library(data.table)
library(ggplot2)
library(ggthemes)


##import data
themedata <- read_csv("IH_ThemesQuant.csv", 
                      col_types = cols(DataAndInfo = col_number(), 
                                       KnowledgeAndPerspective = col_number(), 
                                       ProgramAndOrganization = col_number(), 
                                       Technology = col_number(), 
                                       CommunitiesAndPeople = col_number(), 
                                       Crossdisciplinarity = col_number(), 
                                       Research = col_number(),
                                       Innovation = col_number(), 
                                       Other = col_number()))

##replace NAs with 0
themedata[is.na(themedata)] <- 0


##pivot our data to create a new 'theme' variable
themedatalong <- themedata %>% pivot_longer(cols=c('DataAndInfo', 
                                  'KnowledgeAndPerspective',
                                  'ProgramAndOrganization',
                                  'Technology',
                                  'CommunitiesAndPeople',
                                  'Crossdisciplinarity',
                                  'Research',
                                  'Innovation',
                                  'Other'),
                    names_to='Theme',
                    values_to='Present') 

##subset data so we can plot only those themes present in a given quote
themedatalong <- subset(themedatalong, Present == 1)

##rename 
themedatalong <- themedatalong |>
  mutate(across('Theme', str_replace, 'DataAndInfo', 'Data and Information'),
         across('Theme', str_replace, 'KnowledgeAndPerspective', 'Knowledge and Perspectives'),
         across('Theme', str_replace, 'ProgramAndOrganization', 'Programs and Organizations'),
         across('Theme', str_replace, 'CommunitiesAndPeople', 'Communities and People')
         )
  


##define the colours we want for our themes
##using Tol's accessible palette: https://personal.sron.nl/~pault/#sec:qualitative 
choosecolours <- c("#332288","#88CCEE","#44AA99", "#117733", "#DDCC77", "#CC6677", "#882255","#AA4499","#BBBBBB")

##greyscale option
#choosecolours <- c("#333333","#575757","#6E6E6E", "#818181", "#919191", "#9F9F9F", "#ABABAB","#B7B7B7","#C2C2C2")

##make our plot
p <- ggplot(themedatalong, aes(x=Quote,
                           y=factor(Theme, level=c('Other',
                                                   'Innovation',
                                                   'Research',
                                                   'Crossdisciplinarity',
                                                   'Communities and People',
                                                   'Technology',
                                                   'Programs and Organizations',
                                                   'Knowledge and Perspectives',
                                                   'Data and Information'
                                                   )),
                           color = Theme)
       ) +
  geom_point(size = 6, shape=15) +
  scale_color_manual(breaks = c('Data and Information', 
                                'Knowledge and Perspectives',
                                'Programs and Organizations',
                                'Technology',
                                'Communities and People',
                                'Crossdisciplinarity',
                                'Research',
                                'Innovation',
                                'Other'),
                     values = choosecolours) +
  theme(axis.text.x=element_blank(), 
        axis.ticks.x=element_blank(),
        legend.position = "none",
        axis.title.x = element_text(size=14, face="bold"),
        axis.title.y = element_text(size=14, face="bold"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) + 
  ylab("Themes") +
  xlab("Excerpts") 

p
