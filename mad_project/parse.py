import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mad_project.settings')

import django
django.setup()

import xlrd

from MAD.models import Activities, Categories, act_cat, act_day


def populate():
    
    #Open the spreadsheet with formatted database info
    workbook = xlrd.open_workbook('test.xls')
    worksheet = workbook.sheet_by_name('Sheet1')


    #loop through all rows in the spreadsheet
    #worksheet.nrows    
    for row in range(1, worksheet.nrows):
        
        #function to add info from the first 9 rows into the activity table
        #saves activity object in variable a
        
        a = add_activity(
            name = worksheet.cell(row, 0).value,
            venue = worksheet.cell(row, 1).value,
            postcode = worksheet.cell(row, 2).value,
            agesLower = worksheet.cell(row, 3).value,
            agesUpper = worksheet.cell(row, 4).value,
            contactName = worksheet.cell(row, 5).value,
            contactEmail = worksheet.cell(row, 6).value,
            contactNumber = worksheet.cell(row, 7).value,
            special = worksheet.cell(row, 8).value)

        
        
        #take care of adding categorie(s) to the junction table
        for cat in range(9,13):
            if worksheet.cell(row, cat).value == xlrd.empty_cell.value:
                pass
            else:
                addingCategories = add_cat_to_activity(worksheet.cell(row, cat).value, a)

        
        #take care of adding activities day and times to junction table
        for i in range(13,20):
            if worksheet.cell(row, i).value == xlrd.empty_cell.value:
                pass
            else:
                if i == 13:
                    day = "Monday"
                if i == 14:
                    day = "Tuesday"
                if i == 15:
                    day = "Wednesday"
                if i == 16:
                    day = "Thursday"
                if i == 17:
                    day = "Friday"
                if i == 18:
                    day = "Saturday"
                if i == 19:
                    day = "Sunday"

                timeValue = worksheet.cell(row, i).value

                startValue = timeValue[:5]
                endValue = timeValue[6:]

                addingTimes = add_dayTime_to_activity(a,day,startValue,endValue)
        

#function responsible for recording each activity into the database
def add_activity(name,venue,postcode,agesLower,agesUpper,contactName,contactEmail,contactNumber,special):
    a = Activities.objects.create(name=name)
    a.venue=venue
    a.postcode=postcode
    a.agesLower=agesLower
    a.agesUpper=agesUpper
    a.contactName=contactName
    a.contactEmail=contactEmail
    a.contactNumber=contactNumber
    a.special=special
    a.save()
    return a

#function responsible for matching each new activity with all the categories its associated with
#parameters are activity object plus category name
def add_cat_to_activity(n, activity):
    try:
        c = Categories.objects.get(name=n)
        print "found"

        ac = act_cat.objects.create()
        ac.act = activity
        ac.cat = c
        ac.save()


    except Categories.DoesNotExist:
        print n
        print "No category found"

#function responsible for matching activity with their day and times
def add_dayTime_to_activity(activity, day, start, end):

    actDay = act_day.objects.create()
    actDay.act = activity
    actDay.day = day
    actDay.startTime = start
    actDay.endTime = end
    actDay.save()

# Start execution here!
if __name__ == '__main__':
    print "Starting MAD population script..."
    populate()